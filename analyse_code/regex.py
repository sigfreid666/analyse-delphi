C_RE_UNIT = r'UNIT\s*([\.\w]+)\s*;'
C_RE_INTERFACE = r'INTERFACE\s+'
C_RE_IMPLEMENTATION = r'IMPLEMENTATION\s+'
C_RE_END_FINAL = r'END\s*\.'
C_RE_USES = r'USES[ ]*((?:[^,;]+[ ]*,[ ]*)*[^,;]+)[ ]*;'
C_RE_TYPES = r'TYPE\s'
C_RE_DECL_TYPE = r'([^= ]+)[ ]*=[ ]*([^;]+)[ ]*;'
C_RE_DECL_TYPE_SETOF = r'([^= ]+)[ ]*=[ ]*SET[ ]*OF[ ]*([^;]+)[ ]*;'
C_RE_CLASS = r'(\w+)[ ]*=[ ]*CLASS[ ]*(\([^\)]*\))?.*?END\s*;'
C_RE_CLASS_DEB = r'(\w+)[ ]*=[ ]*(CLASS|RECORD|INTERFACE)[ ]*(\([^\)]*\))?'
C_RE_END = r'END\s*;'
C_RE_RECORD = r'(\w+)[ ]*=[ ]*RECORD[ ]*.*END\s*;'
C_RE_TYPE_PROC_FUNC = r'(\w+)[ ]*=[ ]*(?:REFERENCE)?[ ]*(?:TO)?[ ]*((?:PROCEDURE|FUNCTION)[ ]*\(.*?\)[ ]*(?:OF)?[ ]*(?:OBJECT)?[ ]*);'
C_RE_PARAM = r'\s*(CONST|VAR|OUT)?\s+([^:]+)\s*:\s*([\w<> ]+)\s*;?'
C_RE_FUNCTION_DECL = r'FUNCTION[ ]+([^ \(]+)[ ]*\(([^\)]*)\)[ ]*:[ ]*([^;]*);(?:[ ]*(OVERLOAD|OVERRIDE|VIRTUAL|ABSTRACT)[ ]*;)?'
C_RE_FUNCTION_IMPL = r'FUNCTION[ ]+(%s)[ ]*\(([^\(\)]*)\)[ ]*:[ ]*([^;]*);(?:[ ]*(OVERLOAD|OVERRIDE|VIRTUAL|ABSTRACT)[ ]*;)?'
C_RE_FUNCTION_DECL_S = r'FUNCTION[ ]+([^ \(]+)[ ]*[ ]*:[ ]*([^;]*);(?:[ ]*(OVERLOAD|OVERRIDE|VIRTUAL|ABSTRACT)[ ]*;)?'
C_RE_FUNCTION_IMPL_S = r'FUNCTION[ ]+(%s)[ ]*[ ]*:[ ]*([^;]*);(?:[ ]*(OVERLOAD|OVERRIDE|VIRTUAL|ABSTRACT)[ ]*;)?'
C_RE_PROCEDURE_DECL = r'(?:PROCEDURE|CONSTRUCTOR)[ ]+([^ \(]+)[ ]*\(([^\)]*)\)[ ]*;(?:[ ]*(OVERLOAD|OVERRIDE|VIRTUAL|ABSTRACT)[ ]*;)?'
C_RE_PROCEDURE_IMPL = r'(?:PROCEDURE|CONSTRUCTOR)[ ]+(%s)[ ]*\(([^\)]*)\)[ ]*;(?:[ ]*(OVERLOAD|OVERRIDE|VIRTUAL|ABSTRACT)[ ]*;)?'
C_RE_PROCEDURE_DECL_S = r'(?:PROCEDURE|CONSTRUCTOR)[ ]+([^ \(]+)[ ]*;(?:[ ]*(OVERLOAD|OVERRIDE|VIRTUAL|ABSTRACT)[ ]*;)?'
C_RE_PROCEDURE_IMPL_S = r'(?:PROCEDURE|CONSTRUCTOR)[ ]+(%s)[ ]*;(?:[ ]*(OVERLOAD|OVERRIDE|VIRTUAL|ABSTRACT)[ ]*;)?'
C_RE_PROCEDURE_FUNCTION_DEB = r'(PROCEDURE|CONSTRUCTOR|FUNCTION)[ ]+'

C_RE_GROUPE_FUNCTION_PROCEDURE = [C_RE_FUNCTION_DECL,
                                  C_RE_FUNCTION_DECL_S,
                                  C_RE_PROCEDURE_DECL,
                                  C_RE_PROCEDURE_DECL_S]
