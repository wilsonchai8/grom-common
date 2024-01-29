from transitions import Machine
from .exception_handler import RunError


states_to_name = {
    'modified': '已修改',
    'publishing': '发布中',
    'published': '已发布',
    'publish_failed': '发布失败',
    'rollbacking': '回滚中',
    'rollbacked': '已回滚',
    'rollback_failed': '回滚失败',
    'abandon': '放弃修改',
    'disabled': '禁用',
    'enabled': '启用'
}


class ConfigStatus(object):
    states = list(states_to_name.keys())

    def __init__(self, st='modified'):
        self.machine = Machine(model=self, states=ConfigStatus.states, initial=st, ignore_invalid_triggers=True)

        self.machine.add_transition(source='modified', trigger='modified', dest='modified')
        self.machine.add_transition(source='modified', trigger='publishing', dest='publishing')
        self.machine.add_transition(source='modified', trigger='rollbacking', dest='rollbacking')
        self.machine.add_transition(source='publishing', trigger='published', dest='published')
        self.machine.add_transition(source='publishing', trigger='publish_failed', dest='publish_failed')
        self.machine.add_transition(source='publish_failed', trigger='publishing', dest='publishing')
        # self.machine.add_transition(source='publish_failed', trigger='publish_failed', dest='publish_failed')
        # self.machine.add_transition(source='publish_failed', trigger='published', dest='published')
        self.machine.add_transition(source='publish_failed', trigger='modified', dest='modified')
        self.machine.add_transition(source='rollbacking', trigger='rollbacking', dest='rollbacking')
        self.machine.add_transition(source='rollbacking', trigger='rollbacked', dest='rollbacked')
        self.machine.add_transition(source='rollbacking', trigger='rollback_failed', dest='rollback_failed')
        self.machine.add_transition(source='rollback_failed', trigger='rollbacking', dest='rollbacking')
        # self.machine.add_transition(source='rollback_failed', trigger='rollbacked', dest='rollbacked')
        # self.machine.add_transition(source='rollback_failed', trigger='rollback_failed', dest='rollback_failed')
        self.machine.add_transition(source='rollback_failed', trigger='modified', dest='modified')
        self.machine.add_transition(source='published', trigger='rollbacking', dest='rollbacking')
        self.machine.add_transition(source='published', trigger='publishing', dest='publishing')
        self.machine.add_transition(source='published', trigger='modified', dest='modified')
        self.machine.add_transition(source='rollbacked', trigger='rollbacking', dest='rollbacking')
        self.machine.add_transition(source='rollbacked', trigger='modified', dest='modified')
        self.machine.add_transition(source='rollbacked', trigger='publishing', dest='publishing')

    def switch(self, current):
        pre = self.state
        fn = getattr(self, current)
        if not fn():
            raise RunError(msg='不能从{}状态切换到{}状态'.format(pre, current))

