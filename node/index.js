import fs from 'fs';
import QueueServer from './grpc-queue';

const DIR = 'F:/Games/World_of_Warships_NA';
const MOD_DIR = [DIR, 'bin/2744482/res_mods/0.9.7.0/PnFMods/AutoMod'].join('/');

const PREFIX = {
    Battle: 'battle',
    Mouse: 'mouse',
    Ribbon: 'ribbon',
    Player: 'player',
    Enemy: 'enemy'
};

const server = new QueueServer();
const filenames = [];

function handleMouseLog(path) {
    return new Promise((resolve, reject) => {
        const data = JSON.parse(fs.readFileSync(path).toString('utf-8'));
        console.log('Mouse:', data);    // data.dx, data.dy, data.timestamp
        server.addMouseInput(data);
        resolve();
    });
}

function handlePlayerLog(path) {
    const data = JSON.parse(fs.readFileSync(path).toString('utf-8'));
    server.setPlayer(data);
}

fs.watch(MOD_DIR, (eventType, filename) => {
    if (!filename
        || !(filename.startsWith(PREFIX.Mouse)
             || filename.startsWith(PREFIX.Player)
             || filename.startsWith(PREFIX.Enemy))   // FIXME: map
        || eventType != 'change'
        || filenames.includes(filename)) { return; }

    const path = [MOD_DIR, filename].join('/');

    if (filename.startsWith(PREFIX.Mouse)) {
        filenames.push(filename);
        handleMouseLog(path)
        .then(() => {
            fs.unlink(path, () => {
                const fileIndex = filenames.indexOf(filename);
                if (fileIndex > -1) {
                    filenames.splice(fileIndex, 1);
                }
            });
        });
    }

    if (filename.startsWith(PREFIX.Player)) {
        handlePlayerLog(path);
    }
});

server.start();