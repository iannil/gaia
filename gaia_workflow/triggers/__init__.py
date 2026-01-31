"""
GAIA Workflow - Triggers

触发器模块，管理工作流的触发。
"""

from typing import Dict, List, Callable, Optional, Any
from datetime import datetime
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler

from .dsl import Workflow, Trigger, TriggerType


class TriggerManager:
    """触发器管理器"""

    def __init__(self):
        self._triggers: Dict[str, Trigger] = {}
        self._workflows: Dict[str, Workflow] = {}
        self._callbacks: Dict[str, List[Callable]] = {}
        self._scheduler = None

    def register_workflow(self, workflow: Workflow) -> None:
        """注册工作流"""
        self._workflows[workflow.id] = workflow

        # 注册触发器
        for trigger in workflow.triggers:
            key = f"{workflow.id}:{trigger.type.value}"
            self._triggers[key] = trigger

    def unregister_workflow(self, workflow_id: str) -> None:
        """取消注册工作流"""
        if workflow_id in self._workflows:
            del self._workflows[workflow_id]

        # 删除相关触发器
        keys_to_remove = [k for k in self._triggers if k.startswith(f"{workflow_id}:")]
        for key in keys_to_remove:
            del self._triggers[key]

    def register_callback(
        self,
        trigger_type: TriggerType,
        callback: Callable[[str, Dict[str, Any]], None],
    ) -> None:
        """注册触发回调"""
        if trigger_type.value not in self._callbacks:
            self._callbacks[trigger_type.value] = []
        self._callbacks[trigger_type.value].append(callback)

    def trigger(
        self,
        workflow_id: str,
        trigger_type: TriggerType,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """手动触发工作流"""
        workflow = self._workflows.get(workflow_id)
        if not workflow:
            return False

        # 检查是否有对应的触发器
        has_trigger = any(
            t.type == trigger_type
            for t in workflow.triggers
        )

        if not has_trigger:
            return False

        # 调用回调
        callbacks = self._callbacks.get(trigger_type.value, [])
        for callback in callbacks:
            try:
                callback(workflow_id, context or {})
            except Exception:
                pass

        return True

    def trigger_event(self, event_name: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
        """触发事件"""
        triggered = []

        for workflow_id, workflow in self._workflows.items():
            for trigger in workflow.triggers:
                if (
                    trigger.type == TriggerType.EVENT
                    and trigger.config.get("event") == event_name
                ):
                    if self.trigger(workflow_id, TriggerType.EVENT, context):
                        triggered.append(workflow_id)

        return triggered

    def start_scheduler(self) -> None:
        """启动定时调度器"""
        if self._scheduler is None:
            self._scheduler = BackgroundScheduler()
            self._scheduler.start()

            # 注册定时触发器
            for key, trigger in self._triggers.items():
                if trigger.type == TriggerType.SCHEDULE:
                    workflow_id = key.split(":")[0]
                    cron = trigger.config.get("cron", "")
                    if cron:
                        try:
                            self._scheduler.add_job(
                                lambda: self.trigger(workflow_id, TriggerType.SCHEDULE),
                                'cron',
                                **self._parse_cron(cron),
                            )
                        except Exception:
                            pass

    def stop_scheduler(self) -> None:
        """停止定时调度器"""
        if self._scheduler:
            self._scheduler.shutdown()
            self._scheduler = None

    def _parse_cron(self, cron: str) -> Dict[str, Any]:
        """解析 cron 表达式"""
        # 简化实现，支持 "0 9 * * *" 格式
        parts = cron.split()
        if len(parts) >= 5:
            return {
                "hour": int(parts[1]),
                "minute": int(parts[0]),
            }
        return {}


class EventSystem:
    """事件系统

    管理和分发事件。
    """

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._event_history: List[Dict[str, Any]] = []

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """订阅事件"""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> bool:
        """取消订阅"""
        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(callback)
                return True
            except ValueError:
                pass
        return False

    def emit(
        self,
        event_name: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """触发事件"""
        event = {
            "name": event_name,
            "data": data or {},
            "timestamp": datetime.now().isoformat(),
        }

        # 记录历史
        self._event_history.append(event)

        # 通知监听器
        for callback in self._listeners.get(event_name, []):
            try:
                callback(event)
            except Exception:
                pass

    def get_history(
        self,
        event_name: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """获取事件历史"""
        history = self._event_history

        if event_name:
            history = [e for e in history if e["name"] == event_name]

        return history[-limit:]


# 预定义事件
class Events:
    """预定义事件"""

    # GAIA 事件
    PHASE_STARTED = "gaia.phase.started"
    PHASE_COMPLETED = "gaia.phase.completed"
    PHASE_FAILED = "gaia.phase.failed"

    # Skill 事件
    SKILL_INSTALLED = "gaia.skill.installed"
    SKILL_UPDATED = "gaia.skill.updated"
    SKILL_REMOVED = "gaia.skill.removed"

    # 工作流事件
    WORKFLOW_STARTED = "gaia.workflow.started"
    WORKFLOW_COMPLETED = "gaia.workflow.completed"
    WORKFLOW_FAILED = "gaia.workflow.failed"

    # 文件事件
    FILE_CREATED = "file.created"
    FILE_MODIFIED = "file.modified"
    FILE_DELETED = "file.deleted"


__all__ = [
    "TriggerManager",
    "EventSystem",
    "Events",
]
