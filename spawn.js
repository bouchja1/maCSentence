const cp = require('child_process');

module.exports = (cmd, args = [], options = {}) => {
    process.on('unhandledRejection', err => {
        throw err;
    });

    const result = cp.spawnSync(cmd, args, { stdio: 'pipe', ...options });

    if (result.signal) {
        if (result.signal === 'SIGKILL') {
            console.error(
                'The build failed because the process exited too early. ' +
                'This probably means the system ran out of memory or someone called ' +
                '`kill -9` on the process.'
            );
        } else if (result.signal === 'SIGTERM') {
            console.error(
                'The build failed because the process exited too early. ' +
                'Someone might have called `kill` or `killall`, or the system could ' +
                'be shutting down.'
            );
        }
        throw new Error('Cannot obtain sentences.')
    }

    return result.output;
};
