const Koa = require('koa');
const koaBodyParser = require('koa-bodyparser');
const router = require('@koa/router')();
const path = require('path');

const spawn = require('./spawn');

const app = new Koa();
app.use(koaBodyParser());

const separatorDir = path.join(__dirname, 'separator');

router.post('/sentence', async (ctx, next) => {
    const { text } = ctx.request.body;
    const scriptArgs = [
        `${separatorDir}/separator.py`,
        text
    ];
    // spawn new child process to call the python script
    try {
        let sentencesResultArray = spawn(`python`, scriptArgs, { cwd: process.cwd(), encoding: 'utf-8' });
        sentencesResultArray = sentencesResultArray.filter(sentence => sentence);
        if (sentencesResultArray.length === 1) {
            const [ joinedSeparatedSentences ] = sentencesResultArray;
            ctx.body = {
                sentences: joinedSeparatedSentences.split('\\SEPARATOR')
            }
            ctx.status = 200;
        } else {
            ctx.status = 400;
        }
    } catch (err) {
        console.log("Error: ", err)
        ctx.status = 500;
    }
    await next();
});
app.use(router.routes()); // route middleware

module.exports = app;
