import * as grpc from 'grpc';
import * as protoLoader from '@grpc/proto-loader';
import path from 'path';

Array.prototype.empty = () => this.length == 0;
// Array.prototype.first = () => this.length == 0 ? null : this.shift();
// Array.prototype.clear = () => this.prototype.splice(0, this.length);

const PROTO_PATH = path.join(__dirname, '..', 'proto', 'queue.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const protoDescriptor = grpc.loadPackageDefinition(packageDefinition);

const QueueService = protoDescriptor.wows.QueueService;

class QueueServer {

    constructor() {
        this.player = {
            id: 0, team_id: 0, ship_id: 0,
            health: 1000, max_health: 1000,
            yaw: 0, speed: 0,
            is_visible: true, is_ship_visible: true
        };
        this.enemy = {
            id: 0, team_id: 0, ship_id: 0,
            health: 1000, max_health: 1000,
            yaw: 0, speed: 0,
            is_visible: false, is_ship_visible: false
        };
        this.mouseQueue = [];
        this.keyboardQueue = [];
        this.ribbonQueue = [];
        this.server = new grpc.Server();
        this.server.addService(QueueService.service, {
            getMouseInput: this.getMouseInput,
            getKeyboardInput: this.getKeyboardInput,
            getPlayerInfo: this.getPlayerInfo,
            __mouseQueue: this.mouseQueue,
            __keyboardQueue: this.keyboardQueue,
            __player: this.player,
            __enemy: this.enemy
        });
        this.server.bind('0.0.0.0:61084', grpc.ServerCredentials.createInsecure());
    }

    start() {
        console.log('QueueServer is running at port 61084..');
        this.server.start();
    }

    addMouseInput(mouseInput) {
        this.mouseQueue.push(mouseInput);    // { dx, dy, timestamp }
        console.log('MouseQueue:', this.mouseQueue, this.mouseQueue.length);
    }

    addKeyboardInput(keyboardInput) {
        this.keyboardQueue.push({ timestamp: Date.now(), data: keyboardInput });
    }

    // gRPC Functions
    getMouseInput(call, callback) {
        const queue = this.__mouseQueue.filter(inp => inp.timestamp > call.request.timestamp);
        const mouseInput = queue[0] || { dx: 0, dy: 0 };
        this.__mouseQueue.splice(0, this.__mouseQueue.length);
        callback(null, { data: { ...mouseInput, click: false } });
    }

    getKeyboardInput(call, callback) {
        this.__keyboardQueue = this.__keyboardQueue.filter(inp => inp.timestamp > call.request.timestamp);
        const keyboardInput = this.__keyboardQueue.empty()
                                ? { key: 0 }
                                : this.__keyboardQueue.shift();
        callback(null, keyboardInput);
    }

    getPlayerInfo(call, callback) {
        callback(null, { data: call.request.is_enemy
                                ? this.__enemy
                                : this.__player });
    }

    setPlayer(player) {
        Object.assign(this.player, player);
    }

    setEnemy(enemy) {
        Object.assign(this.enemy, enemy);
    }
}

export default QueueServer;