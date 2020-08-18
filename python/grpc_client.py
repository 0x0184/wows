#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time

import grpc

import queue_pb2
import queue_pb2_grpc
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class QueueClient:

    def __init__(self, queue=None, addr='127.0.0.1', port=61084):
        channel = grpc.insecure_channel('%s:%d' % (addr, port))
        self.stub = queue_pb2_grpc.QueueServiceStub(channel)

    def get_player_info(self, is_enemy=False):
        try:
            request = queue_pb2.PlayerInfoRequest(is_enemy=is_enemy)
            info = self.stub.GetPlayerInfo(request)
            return info.data
        except grpc._channel._InactiveRpcError as e:
            print('[PlayerInfo] grpc._channel._InactiveRpcError:', e)
        except Exception as e:
            print('[PlayerInfo] Exception:', e)
        return queue_pb2.PlayerInfo()

    def get_mouse_input(self, timestamp=0):
        if not timestamp:
            timestamp = int(time.time() * 1000) - 1000
        try:
            request = queue_pb2.MouseInputRequest(timestamp=timestamp)
            inp = self.stub.GetMouseInput(request)
            # print('inp.data:', inp.data.dx, inp.data.dy)
            return inp.data
        except grpc._channel._InactiveRpcError as e:
            print('[Mouse] grpc._channel._InactiveRpcError:', e)
        except Exception as e:
            print('[Mouse] Exception:', e)
        return queue_pb2.MouseInput()


if __name__ == "__main__":
    client = QueueClient()
    client.get_player_info()
    client.get_player_info(True)
