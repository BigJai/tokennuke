"""Language specifications for tree-sitter AST extraction.

Each spec defines:
- extensions: File extensions for this language
- tree_sitter_name: Name used by tree-sitter-language-pack
- function_types: AST node types that define functions
- class_types: AST node types that define classes
- call_types: AST node types that represent function calls
- name_field: Field name for extracting the symbol name
- body_field: Field name for the function/class body
- docstring_type: AST node type for docstrings (if any)
- decorator_type: AST node type for decorators (if any)
- string_type: AST node type for string literals
- comment_type: AST node type for comments
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LanguageSpec:
    """Tree-sitter node type mappings for a language."""

    name: str
    tree_sitter_name: str
    extensions: list[str]
    function_types: list[str]
    class_types: list[str]
    call_types: list[str]
    name_field: str = 'name'
    body_field: str = 'body'
    parameters_field: str = 'parameters'
    return_type_field: str = 'return_type'
    docstring_type: str = ''
    decorator_type: str = ''
    string_type: str = 'string'
    comment_type: str = 'comment'
    # Additional node types that count as "type definitions"
    type_types: list[str] = field(default_factory=list)
    # Constant/variable node types
    constant_types: list[str] = field(default_factory=list)
    # Interface/protocol types
    interface_types: list[str] = field(default_factory=list)


LANGUAGES: dict[str, LanguageSpec] = {
    'python': LanguageSpec(
        name='python',
        tree_sitter_name='python',
        extensions=['.py', '.pyi'],
        function_types=['function_definition'],
        class_types=['class_definition'],
        call_types=['call'],
        parameters_field='parameters',
        return_type_field='return_type',
        docstring_type='expression_statement',  # first child string = docstring
        decorator_type='decorator',
        constant_types=['assignment'],  # top-level MODULE_CONSTANT = ...
    ),
    'javascript': LanguageSpec(
        name='javascript',
        tree_sitter_name='javascript',
        extensions=['.js', '.jsx', '.mjs', '.cjs'],
        function_types=[
            'function_declaration',
            'arrow_function',
            'method_definition',
            'generator_function_declaration',
        ],
        class_types=['class_declaration'],
        call_types=['call_expression'],
        parameters_field='parameters',
        return_type_field='',
        decorator_type='decorator',
        constant_types=['lexical_declaration', 'variable_declaration'],
    ),
    'typescript': LanguageSpec(
        name='typescript',
        tree_sitter_name='typescript',
        extensions=['.ts', '.tsx'],
        function_types=[
            'function_declaration',
            'arrow_function',
            'method_definition',
            'generator_function_declaration',
        ],
        class_types=['class_declaration'],
        call_types=['call_expression'],
        parameters_field='parameters',
        return_type_field='return_type',
        decorator_type='decorator',
        type_types=['type_alias_declaration'],
        interface_types=['interface_declaration'],
        constant_types=['lexical_declaration', 'variable_declaration'],
    ),
    'go': LanguageSpec(
        name='go',
        tree_sitter_name='go',
        extensions=['.go'],
        function_types=['function_declaration', 'method_declaration'],
        class_types=[],  # Go has no classes
        call_types=['call_expression'],
        parameters_field='parameters',
        return_type_field='result',
        type_types=['type_declaration'],
        interface_types=['type_declaration'],  # filtered by spec child
        constant_types=['const_declaration', 'var_declaration'],
    ),
    'rust': LanguageSpec(
        name='rust',
        tree_sitter_name='rust',
        extensions=['.rs'],
        function_types=['function_item'],
        class_types=['struct_item', 'enum_item'],
        call_types=['call_expression'],
        parameters_field='parameters',
        return_type_field='return_type',
        type_types=['type_item'],
        interface_types=['trait_item'],
        constant_types=['const_item', 'static_item'],
        comment_type='line_comment',
    ),
    'java': LanguageSpec(
        name='java',
        tree_sitter_name='java',
        extensions=['.java'],
        function_types=['method_declaration', 'constructor_declaration'],
        class_types=['class_declaration', 'enum_declaration'],
        call_types=['method_invocation'],
        parameters_field='parameters',
        return_type_field='type',
        decorator_type='marker_annotation',
        interface_types=['interface_declaration'],
        constant_types=['field_declaration'],
    ),
    'c': LanguageSpec(
        name='c',
        tree_sitter_name='c',
        extensions=['.c', '.h'],
        function_types=['function_definition'],
        class_types=['struct_specifier'],
        call_types=['call_expression'],
        name_field='declarator',
        parameters_field='parameters',
        return_type_field='type',
        type_types=['type_definition'],
        constant_types=['declaration'],
    ),
    'cpp': LanguageSpec(
        name='cpp',
        tree_sitter_name='cpp',
        extensions=['.cpp', '.cxx', '.cc', '.hpp', '.hxx', '.hh'],
        function_types=['function_definition'],
        class_types=['class_specifier', 'struct_specifier'],
        call_types=['call_expression'],
        name_field='declarator',
        parameters_field='parameters',
        return_type_field='type',
        type_types=['type_definition', 'alias_declaration'],
        constant_types=['declaration'],
    ),
    'csharp': LanguageSpec(
        name='csharp',
        tree_sitter_name='c_sharp',
        extensions=['.cs'],
        function_types=['method_declaration', 'constructor_declaration'],
        class_types=['class_declaration', 'struct_declaration', 'enum_declaration'],
        call_types=['invocation_expression'],
        parameters_field='parameters',
        return_type_field='type',
        decorator_type='attribute_list',
        interface_types=['interface_declaration'],
        constant_types=['field_declaration', 'property_declaration'],
    ),
    'ruby': LanguageSpec(
        name='ruby',
        tree_sitter_name='ruby',
        extensions=['.rb', '.rake', '.gemspec'],
        function_types=['method', 'singleton_method'],
        class_types=['class', 'module'],
        call_types=['call', 'method_call'],
        parameters_field='parameters',
        return_type_field='',
        constant_types=['assignment'],
    ),
}

# Build extension → language lookup
_EXT_MAP: dict[str, str] = {}
for lang_name, spec in LANGUAGES.items():
    for ext in spec.extensions:
        _EXT_MAP[ext] = lang_name


def get_language_for_file(file_path: str | Path) -> str | None:
    """Get the language name for a file based on its extension."""
    suffix = Path(file_path).suffix.lower()
    return _EXT_MAP.get(suffix)


def get_spec(language: str) -> LanguageSpec | None:
    """Get the LanguageSpec for a language name."""
    return LANGUAGES.get(language)
