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
        const sentencesArray = spawn(`python`, scriptArgs, { cwd: process.cwd(), encoding: 'utf-8' });
        if (sentencesArray && sentencesArray.length) {
            const sentences = sentencesArray.filter(sentence => sentence).map(sentence => {
                return sentence.replace(/^\d\./, '');
            });
            if (sentences.length === 1) {
                const [ notSplitSentences ] = sentences;
                ctx.body = {
                    sentences: notSplitSentences.split('\\SEPARATOR')
                }
                ctx.status = 200;
            } else {
                ctx.status = 400;
            }
        } else {
            ctx.status = 500;
        }
    } catch (err) {
        console.log("Error: ", err)
        ctx.status = 500;
    }
    await next();
});
app.use(router.routes()); // route middleware

module.exports = app;
