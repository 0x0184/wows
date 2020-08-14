import fs from 'fs';

const DIR = 'F:/Games/World_of_Warships_NA';
const MOD_DIR = [DIR, 'bin/2744482/res_mods/0.9.7.0/pnFMods/AutoMod'].join('/');

const PREFIX = {
    Battle: 'battle',
    Mouse: 'mouse',
    Ribbon: 'ribbon'
};

const filenames = [];

fs.watch(MOD_DIR, (eventType, filename) => {
    if (!filename || eventType != 'change') { return; }
    if (filenames.includes(filename)) { return; }
    filenames.push(filename);

    const path = [MOD_DIR, filename].join('/');
    const data = JSON.parse(fs.readFileSync(path).toString('utf-8'));
    console.log('Mouse:', data);
    fs.unlink(path, () => {
        const fileIndex = filenames.indexOf(filename);
        if (fileIndex > -1) {
            filenames.splice(fileIndex, 1);
        }
    });
});