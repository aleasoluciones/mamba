import ast


class TransformToSpecsNodeTransformer(ast.NodeTransformer):
    PENDING_EXAMPLE_GROUPS = ('_description', '_context')
    EXAMPLE_GROUPS = ('description', 'context') + PENDING_EXAMPLE_GROUPS
    EXAMPLES = ('it', '_it')
    HOOKS = ('before', 'after')

    def visit_With(self, node):
        super(TransformToSpecsNodeTransformer, self).generic_visit(node)

        name = node.context_expr.func.id

        if name in self.EXAMPLE_GROUPS:
            return self._transform_to_example_group(node, name)
        if name in self.EXAMPLES:
            return self._transform_to_example(node, name)
        if name in self.HOOKS:
            return self._transform_to_hook(node, name)

        return node

    def _transform_to_example_group(self, node, name):
        if self._subject_is_a_class(node):
            node.body.insert(0, ast.Assign(targets=[ast.Name(id='_subject_class', ctx=ast.Store())], value=node.context_expr.args[0]))

        return ast.copy_location(ast.ClassDef(name=self._description_name(node, name), bases=[], body=node.body, decorator_list=[]), node)

    def _description_name(self, node, name):
        if isinstance(node.context_expr.args[0], ast.Str):
            description_name = node.context_expr.args[0].s
        elif isinstance(node.context_expr.args[0], ast.Attribute):
            description_name = node.context_expr.args[0].attr
        else:
            description_name = node.context_expr.args[0].id

        if name in self.PENDING_EXAMPLE_GROUPS:
            description_name += '__pending'

        description_name += '__description'

        return description_name

    def _subject_is_a_class(self, node):
        return not isinstance(node.context_expr.args[0], ast.Str)

    def _transform_to_example(self, node, name):
        example = node.context_expr.args[0].s
        return ast.copy_location(ast.FunctionDef(name=name + ' ' + example, args=ast.arguments(args=[ast.Name(id='self', ctx=ast.Param())], vararg=None, kwarg=None, defaults=[]), body=node.body, decorator_list=[]), node)

    def _transform_to_hook(self, node, name):
        when = node.context_expr.args[0].s
        return ast.copy_location(ast.FunctionDef(name=name + '_' + when, args=ast.arguments(args=[ast.Name(id='self', ctx=ast.Param())], vararg=None, kwarg=None, defaults=[]), body=node.body, decorator_list=[]), node)

