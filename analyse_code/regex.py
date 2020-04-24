C_RE_UNIT = r'UNIT\s*([\.\w]+)\s*;'
C_RE_INTERFACE = r'INTERFACE\s+'
C_RE_IMPLEMENTATION = r'IMPLEMENTATION\s+'
C_RE_END_FINAL = r'END\s*\.'
C_RE_USES = r'USES[ ]*((?:[^,;]+[ ]*,[ ]*)*[^,;]+)[ ]*;'
C_RE_TYPES = r'TYPE\s'
C_RE_DECL_TYPE_CLASS_OF = r'([^= ]+)\s*=\s*class\s+of\s+\w+;'
C_RE_DECL_TYPE = r'([^= ]+)[ ]*=[ ]*([^;]+)[ ]*;'
C_RE_DECL_TYPE_SETOF = r'([^= ]+)[ ]*=[ ]*SET[ ]*OF[ ]*([^;]+)[ ]*;'
C_RE_CLASS = r'(\w+)[ ]*=[ ]*CLASS[ ]*(?:\(([^\)]*)\))?.*?END\s*;'
C_RE_CLASS_DEB = r'(\w+)[ ]*=[ ]*(CLASS|RECORD|INTERFACE)[ ]*(?!of)(?:abstract)?\s*(?:\(([^\)]*)\))?'
C_RE_END = r'END\s*;'
C_RE_RECORD = r'(\w+)[ ]*=[ ]*RECORD[ ]*.*END\s*;'
C_RE_TYPE_PROC_FUNC = r'(\w+)[ ]*=[ ]*(?:REFERENCE)?[ ]*(?:TO)?[ ]*((?:PROCEDURE|FUNCTION)[ ]*\(.*?\)[ ]*(?:OF)?[ ]*(?:OBJECT)?[ ]*);'
C_RE_PARAM = r'\s*(CONST|VAR|OUT)?\s+([^:]+)\s*:\s*([\w<> ]+)\s*;?'
C_RE_VERB_END_FUNC = r'(?:[ ]*(OVERLOAD|OVERRIDE|VIRTUAL|ABSTRACT|STATIC|INLINE|stdcall|deprecated(?:\s+\'[^\']*?\')?)[ ]*;)*'
C_RE_FUNCTION_DECL = r'(?:CLASS\s+)?(FUNCTION|OPERATOR)[ ]+([^ \(]+)[ ]*\(([^\)]*)\)[ ]*:[ ]*([^;]*);' + C_RE_VERB_END_FUNC
C_RE_FUNCTION_IMPL = r'(?:CLASS\s+)?(FUNCTION|OPERATOR)[ ]+(%s)[ ]*\(([^\(\)]*)\)[ ]*:[ ]*([^;]*);' + C_RE_VERB_END_FUNC
C_RE_FUNCTION_DECL_S = r'(?:CLASS\s+)?(FUNCTION|OPERATOR)[ ]+([^ \(]+)[ ]*[ ]*:[ ]*([^;]*);' + C_RE_VERB_END_FUNC
C_RE_FUNCTION_IMPL_S = r'(?:CLASS\s+)?(FUNCTION|OPERATOR)[ ]+(%s)[ ]*[ ]*:[ ]*([^;]*);' + C_RE_VERB_END_FUNC
C_RE_PROCEDURE_DECL = r'(?:CLASS\s+)?(?:PROCEDURE|CONSTRUCTOR|DESTRUCTOR)[ ]+([^ \(]+)[ ]*\(([^\)]*)\)[ ]*;' + C_RE_VERB_END_FUNC
C_RE_PROCEDURE_IMPL = r'(?:CLASS\s+)?(?:PROCEDURE|CONSTRUCTOR|DESTRUCTOR)[ ]+(%s)[ ]*\(([^\)]*)\)[ ]*;' + C_RE_VERB_END_FUNC
C_RE_PROCEDURE_DECL_S = r'(?:CLASS\s+)?(?:PROCEDURE|CONSTRUCTOR|DESTRUCTOR)[ ]+([^ \(]+)[ ]*;' + C_RE_VERB_END_FUNC
C_RE_PROCEDURE_IMPL_S = r'(?:CLASS\s+)?(?:PROCEDURE|CONSTRUCTOR|DESTRUCTOR)[ ]+(%s)[ ]*;' + C_RE_VERB_END_FUNC
C_RE_PROCEDURE_FUNCTION_DEB = r'(PROCEDURE|CONSTRUCTOR|FUNCTION|DESTRUCTOR)[ ]+'
C_RE_SECTION_CLASS = r'(PUBLIC|PRIVATE|PROTECTED|PUBLISHED)\s+'
C_RE_VAR = r'((?:\w+\,?\s*)+):\s*([^;]+?)\s*;'
C_RE_VAR_RECORD = r'((?:\w+\,?\s*)+):\s*(record\s*case\s+\w+\s+of.*?end;)'
C_RE_VAR_RECORD_2 = r'([^;]+?)\s*;'
C_RE_PROPERTY = r'PROPERTY\s+(\w+)(\[Index\s*:\s*\w+\s*\])?\s*:\s*(\w+)\s*(?:(READ)\s*(\w+))?\s*(?:(WRITE)\s*(\w+))?\s*(?:(IMPLEMENTS)\s*(\w+))?;'
C_RE_SECTION_CONST = r'CONST\s+'
C_RE_DEF_CONST = r'(\w+)\s*(?:([^=;]+)\s*)?=\s*([^;]+);'
C_RE_SECTION_RESOURCE = r'RESOURCESTRING\s+'
C_RE_DEF_RESOURCE = r'(\w+)\s*=\s*([^;]+);'
C_RE_SECTION = r'(IMPLEMENTATION|TYPE|CONST|RESOURCESTRING|PROCEDURE|FUNCTION)\s+'
C_RE_GUID = r'\[\s*\'[^\']*\'\s*\]'
C_RE_CASE_TYPE = r'case\s+\w+\s+of(\s+\w+\:\s*\([^\)]*\);)*'
C_RE_SECTION_VAR = r'VAR\s'