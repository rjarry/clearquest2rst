'''
Created on 15 mars 2011

@author: s0030382
'''
from docutils.parsers.rst.directives.tables import Table
from docutils.parsers.rst import directives, DirectiveError
from docutils import statemachine, nodes

import win32com.client as COM
import re
SUBST_REF_REX = re.compile(r'\|(.+?)\|', re.DOTALL)

class Clearquest(Table):
    option_spec = {
        'username': directives.unchanged_required,
        'password': directives.unchanged_required,
        'db_name': directives.unchanged_required,
        'db_set': directives.unchanged_required,
        'params': directives.unchanged
    }

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    
    session = None

    directive_name = "clearquest"


    def run(self):
        try:
            self.resolve_substitutions_refs()
            session = self.open_clearquest_session(username=self.options.get("username", ""), 
                                                   password=self.options.get("password", ""), 
                                                   db_name=self.options.get("db_name", ""), 
                                                   db_set=self.options.get("db_set", ""))
            queryname = self.arguments[0]
            parameters = self.extract_params()

            columns, records = self.run_clearquest_query(session, queryname, parameters)
            
            col_widths = self.get_column_widths(header=columns, content=records)
            table_head = [ self.create_row(columns) ]
            table_body = [ self.create_row(line) for line in records ]
        
        except Exception, detail:
            if isinstance(detail, DirectiveError):
                message = detail.msg
            else:
                message = str(detail)
            error = self.state_machine.reporter.error(
                'Error with query data in "%s" directive:\n%s'
                % (self.name, message), nodes.literal_block(
                self.block_text, self.block_text), line=self.lineno)
            return [error]
        
        table = (col_widths, table_head, table_body)
        table_node = self.state.build_table(table, self.content_offset)
        table_node['classes'] += self.options.get('class', [])
        
        return [table_node]

    def create_row(self, line):
        row = []
        
        for cell_text in line:
            row.append(
                (0, 0, 0, statemachine.StringList(cell_text.splitlines()))
            )
            
        return row

    def get_column_widths(self, header, content):
        widths = [0] * len(header)
        
        for i in range(len(header)):
            if len(header[i]) > widths[i]:
                widths[i] = len(header[i])

        for row in content:
            for i in range(len(row)):
                if len(row[i]) > widths[i]:
                    widths[i] = len(row[i])
        return widths

    def run_clearquest_query(self, session, queryname, parameters):
        workspace = session.GetWorkSpace
        query = workspace.GetQueryDef(queryname)
        resultset = session.BuildResultSet(query)
        nb_params = resultset.GetNumberOfParams
        if nb_params:
            errors = []
            for i in range(1, nb_params + 1):
                param_name = resultset.GetParamLabel(i)
                try:
                    param_value = parameters[param_name]
                except:
                    errors.append("'%s'" % param_name)
                resultset.AddParamValue(i, param_value)
            if errors:
                params = ", ".join(errors) 
                raise self.error("Missing parameters '%s' to query '%s'" % (params, queryname))
    
        resultset.Execute()
        
        status = resultset.MoveNext
        
        nbcol = resultset.GetNumberOfColumns - 1 # this is silly, but first column is reserved
    
        records = []
        columns = [ fieldDef.Label for fieldDef in query.QueryFieldDefs ][1:]
        
        if status != 1:
            # No results from ClearQuest query, we fill one line with dashes
            records.append(list("-" * len(columns)))
    
        while status == 1:
            records.append([ resultset.GetColumnValue(i) for i in range(2, nbcol + 2) ])
            status = resultset.MoveNext
    
        return columns, records

    def open_clearquest_session(self, username, password, db_name, db_set):
        if not self.session:
            self.session = COM.dynamic.Dispatch("CLEARQUEST.SESSION")
            self.session.UserLogon(username, password, db_name, 2, db_set) # '2' stands for "private session"
        return self.session
    
    def extract_params(self):
        params_dict = {}
        params = self.options.get("params")
        if params:
            for p in params.split(","):
                p_name, p_value = p.split("=")
                params_dict[p_name.strip()] = p_value.strip()
        return params_dict

    def resolve_substitutions_refs(self):
        def _subst_ref_match(match):
            return self.state.document.substitution_defs[match.group(1)].astext()
        
        for opt_name in self.options.keys():
            opt_val = unicode(self.options[opt_name])
            opt_val, _ = SUBST_REF_REX.subn(_subst_ref_match, opt_val)
            self.options[opt_name] = opt_val
