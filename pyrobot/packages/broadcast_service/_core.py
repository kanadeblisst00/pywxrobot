# Copyright (c) 2023 Zeeland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/broadcast-service
# Contact Email: zeeland@foxmail.com

import time
from pydantic import BaseModel, validator
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List, Callable, Any, Union

from .singleton import Singleton

__all__ = ['broadcast_service', 'BroadcastService']


def _invoke_callback(
        callback: Callable,
        thread_pool: ThreadPoolExecutor,
        enable_async: bool = True,
        *args,
        **kwargs
) -> Any:
    future = thread_pool.submit(callback, *args, **kwargs)


class BaseBroadcastService(metaclass=Singleton):
    """
    This class implements broadcast mode, you can import the instance by single class.
    By BroadcastService, you can send topic message,it will automatically execute the
    callback function if some classes subscribe the topic.

    Example:
    ---------------------------------------------------------------------------------
    from broadcast_service import broadcast_service

    def handle_msg(params):
        print(params)

    if __name__ == '__main__':
        info = 'This is very important msg'

        # listen topic
        broadcast_service.subscribe('Test', handle_msg)

        # publish broadcast
        broadcast_service.publish('Test', info)
    ---------------------------------------------------------------------------------
    """

    def __init__(self):
        """
        pubsub_channels is the dict to store publish/subscribe data.
        pubsub_channels example:

        pubsub_channels = {
            'my_topic': [callback_function1: Callable,callback_function2: Callable]
            '__all__': [callback_function3: Callable]
        }
        """
        self.pubsub_channels: dict = {
            '__all__': []
        }
        self.enable_async: bool = True
        self.thread_pool = ThreadPoolExecutor(max_workers=100)
        # function renaming
        self.subscribe = self.listen
        self.on = self.listen
        self.publish = self.broadcast
        self.emit = self.broadcast
        self.unsubscribe = self.stop_listen
        self.off = self.stop_listen
        self.on_subscribe = self.on_listen
        self.subscribe_all = self.listen_all
        self.publish_all = self.broadcast_all

    def listen(self, topics: List[str], callback: Callable):
        """
        listen topics.
        """
        if type(topics) == str:
            self._invoke_listen_topic(topics, callback)
        elif type(topics) == list:
            for topic in topics:
                self._invoke_listen_topic(topic, callback)
        else:
            raise ValueError("Unknown broadcast-service error, please submit "
                             "issue to https://github.com/Undertone0809/broadcast-service/issues")

    def listen_all(self, callback: Callable):
        """
        '__all__' is a special topic. It can receive any topic message.
        """
        self._invoke_listen_topic('__all__', callback)

    def broadcast(self, topics: List[str], *args, **kwargs):
        """
        Launch broadcast on the specify topic. If all subscribe callback finish, it will call finish_callback.
        """
        if type(topics) == str:
            self._invoke_broadcast_topic(topics, *args, **kwargs)
        elif type(topics) == list:
            for topic in topics:
                self._invoke_broadcast_topic(topic, *args, **kwargs)
        else:
            raise ValueError("Unknown broadcast-service error, please submit "
                             "issue to https://github.com/Undertone0809/broadcast-service/issues")

    def broadcast_all(self, *args, **kwargs):
        """
        All topics listened on will be called back.
        Attention: Not all callback function will be called. If your publisher callback
        and your subscriber callback takes different arguments, your callback function
        will not be executed.
        """
        for topic in self.pubsub_channels.keys():
            self._invoke_broadcast_topic(topic, *args, **kwargs)

    def _invoke_listen_topic(self, topic_name: str, callback: Callable):
        if topic_name not in self.pubsub_channels.keys():
            self.pubsub_channels[topic_name] = []

        if callback not in self.pubsub_channels[topic_name]:
            self.pubsub_channels[topic_name].append(callback)

    def _invoke_broadcast_topic(self, topic_name: str, *args, **kwargs):
        if topic_name not in self.pubsub_channels.keys():
            self.pubsub_channels[topic_name] = []

        for item in self.pubsub_channels[topic_name]:
            self._final_invoke_listen_callback(item, *args, **kwargs)

        for item in self.pubsub_channels['__all__']:
            if item not in self.pubsub_channels[topic_name]:
                self._final_invoke_listen_callback(item, *args, **kwargs)

    def _final_invoke_listen_callback(self, callback: Callable, *args, **kwargs) -> Any:
        return _invoke_callback(callback, self.thread_pool, self.enable_async, *args, **kwargs)

    def stop_listen(self, topic_name: str, callback: Callable):
        if topic_name not in self.pubsub_channels.keys():
            raise RuntimeError("you didn't listen the topic:", topic_name)
        if callback not in self.pubsub_channels[topic_name]:
            pass
        else:
            self.pubsub_channels[topic_name].remove(callback)

    def on_listen(self, topics: Optional[List[str]] = None) -> Callable:
        """Decorator to listen specify topic. If topics is none, then listen all topics has exits.

        Args:
            topics: topic list, you can input topic like: ["topic1", "topic2"].

        Returns:
            return callback functions

        Examples:
            @broadcast_service.on_listen('topic1')
            def handle_all_msg():
                # your code

            @broadcast_service.on_listen(['topic1'])
            def handle_all_msg():
                # your code

            @broadcast_service.on_listen(['topic1','topic2'])
            def handle_all_msg():
                # your code

            @broadcast_service.on_listen()
            def handle_all_msg(*args, **kwargs):
                # your code

        Attention:
            Your params should keep '*args, **kwargs'. If you publish a topic take arguments,
            the callback function you handle should take arguments, otherwise it will not be called back.
        """

        def decorator(fn: Callable) -> Callable:
            if not topics:
                self.listen_all(fn)
            elif type(topics) == str or list:
                self.listen(topics, fn)

            def inner(*args, **kwargs) -> Callable:
                ret = fn(*args, **kwargs)
                return ret

            return inner

        return decorator


PUBLISHER_CALLBACK_STATUS = {
    "INIT": 'initialization',
    "RUNNING": "running",
    "END": "end"
}


class PublisherDispatchConfig(BaseModel):
    status: str = PUBLISHER_CALLBACK_STATUS["INIT"]
    """life cycle of publisher callback"""
    counter: int = 1
    """Record num of executions for publisher has call publish"""
    num_of_executions: int = 1
    """It indicating the number of times the same topic is published at once"""
    interval: float = 0
    """interval"""
    subscriber_callback_results: Union[dict, List] = []
    """Used to store the return values of all callback functions for subscribers."""
    callback: Optional[Callable] = None
    """Your publisher will obtain the callback and subscriber parameters after the callback function
    of all subscribers callback is completed."""
    enable_final_return: bool = False
    """This parameter indicates whether you want to call the publisher callback after calling the topic 
    n times, or call the publisher callback after each topic publishing."""
    split_parameters: Optional[List[Any]] = None
    """If you initiate multiple calls and want to pass different parameters to the subscriber in each 
    call, you can use this parameter for parameter passing. Additionally, when you use this parameter, 
    you do not need to pass any parameters in the broadcast() function."""

    @property
    def start_publisher_callback_or_not(self) -> bool:
        if self.status == PUBLISHER_CALLBACK_STATUS["END"]:
            return False
        if not self.enable_final_return:
            return True
        if self.enable_final_return and self.counter == self.num_of_executions:
            return True
        return False

    @validator("num_of_executions")
    def check_num_of_executions(cls, v):
        if v <= 0 or type(v) != int:
            raise ValueError("num_of_execution must be a positive integer")
        return v

    @validator("interval")
    def check_interval(cls, v):
        if v < 0 or type(v) not in [int, float]:
            raise ValueError("interval must be a positive float")
        return v

    @validator("split_parameters")
    def check_split_parameters(cls, v):
        if v and len(v) < cls.num_of_executions:
            raise ValueError("The length of split_parameters must be the same as num_of_executions")
        return v

    def get_num_of_executions(self) -> int:
        if self.status == PUBLISHER_CALLBACK_STATUS["END"]:
            return 1
        return self.num_of_executions

    def finish_callback(self):
        self.status = PUBLISHER_CALLBACK_STATUS["END"]

    def append_sub_callback_results(self, value: Any):
        self.subscriber_callback_results.append(value)


class PublisherDispatchConfigManager(metaclass=Singleton):
    def __init__(self):
        self.publisher_callbacks: List[PublisherDispatchConfig] = []

    def get_latest_publisher_callback(self) -> PublisherDispatchConfig:
        return self.publisher_callbacks[-1]

    def create_publisher_callback(self, **kwargs):
        self.publisher_callbacks.append(PublisherDispatchConfig(**kwargs))


class BroadcastService(BaseBroadcastService):
    def __init__(self):
        super().__init__()
        self.publish_dispatch_config_manager = PublisherDispatchConfigManager()
        self.cur_publisher_dispatch_config: PublisherDispatchConfig = PublisherDispatchConfig()

        self.enable_config = False
        """Enable_config is True when you use `broadcast_service.config(**config).publish(topic_name,**params)`
        to publish topic. It indicates whether you need to enable complex configurations to schedule 
        publishing topics."""

    def config(
            self,
            num_of_executions: int = 1,
            callback: Optional[Callable] = None,
            enable_final_return: bool = False,
            interval: float = 0,
            split_parameters: Optional[List[Any]] = None
    ) -> 'BroadcastService':
        """Provide more complex topic publish mode

        Args:
            num_of_executions: default is 1, indicating the number of times the same topic is published at once
            callback: default is None. You can get callback and the parameters of subscriber
                after all subscribers' callback functions have been completed.
            enable_final_return: default is False, it means you can get callback after you publish
                n times topic. In this case, finish_callback params is store in *args rather than **kwargs.
            interval: publish interval. Unit seconds.
            split_parameters: If you initiate multiple calls and want to pass different parameters to the subscriber
                in each call, you can use this parameter for parameter passing. Additionally, when you use this
                parameter, you do not need to pass any parameters in the broadcast() function.
        Returns:
            Returns current object, which is used to call broadcast with configuration.
        """
        self.enable_config = True
        self.publish_dispatch_config_manager.create_publisher_callback(
            num_of_executions=num_of_executions,
            callback=callback,
            enable_final_return=enable_final_return,
            interval=interval,
            status=PUBLISHER_CALLBACK_STATUS['RUNNING'],
            split_parameters=split_parameters
        )
        return self

    def broadcast(self, topics: List[str], *args, **kwargs):
        if self.enable_config:
            self.cur_publisher_dispatch_config = self.publish_dispatch_config_manager.get_latest_publisher_callback()

        for i in range(self.cur_publisher_dispatch_config.get_num_of_executions()):
            if self.cur_publisher_dispatch_config.split_parameters:
                kwargs.update(
                    {"split_parameter": self.cur_publisher_dispatch_config.split_parameters[i]}
                )
            super().broadcast(topics, *args, **kwargs)
            self.cur_publisher_dispatch_config.counter += 1
            time.sleep(self.cur_publisher_dispatch_config.interval)

        self.enable_config = False

    def _invoke_finish_callback(self):
        if self.cur_publisher_dispatch_config.callback:
            self._final_invoke_listen_callback(
                self.cur_publisher_dispatch_config.callback,
                *self.cur_publisher_dispatch_config.subscriber_callback_results
            )
        if self.cur_publisher_dispatch_config.counter == self.cur_publisher_dispatch_config.num_of_executions:
            self.cur_publisher_dispatch_config.finish_callback()

    def _invoke_broadcast_topic(self, topic_name: str, *args, **kwargs):
        super()._invoke_broadcast_topic(topic_name, *args, **kwargs)

        if self.enable_config and self.cur_publisher_dispatch_config.start_publisher_callback_or_not:
            self._invoke_finish_callback()

    def _final_invoke_listen_callback(self, callback: Callable, *args, **kwargs):
        result = super()._final_invoke_listen_callback(callback, *args, **kwargs)

        if result:
            self.cur_publisher_dispatch_config.append_sub_callback_results(result)


broadcast_service = BroadcastService()
