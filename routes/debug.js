const OpenAI = require('openai');
require('dotenv').config();

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

async function CodeDebuger(req, res) {
    const { code,currentLanguage} = req.body;
    
    if (!code) { res.status(404).send("code neeed to be pass") }
    else {
        try {
            const chatCompletion = await openai.chat.completions.create({
                messages: [{ role: "user", content: `Debug the following ${currentLanguage} code: \n\n${code}` }],
                model: "gpt-3.5-turbo",
                stop: null,
            });
            res.status(200).send({ code: chatCompletion.choices[0].message })

        } catch (error) {
            res.status(500).json({ error: 'Internal Server Error' });
        }
    }
};

module.exports = CodeDebuger

