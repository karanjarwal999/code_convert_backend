const OpenAI = require('openai');
require('dotenv').config();

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

async function CodeConverter(req, res) {
    const { code, targetLanguage,currentLanguage} = req.body;
    if (!targetLanguage) { res.status(404).send("targetLanguage neeed to be pass") }
    else if (!code) { res.status(404).send("code neeed to be pass") }
    else {
        try {
            const chatCompletion = await openai.chat.completions.create({
                messages: [{ role: "user", content: `Convert the following ${currentLanguage} code to ${targetLanguage}: \n\n${code}` }],
                model: "gpt-3.5-turbo",
                stop: null,
            });
            console.log(chatCompletion.choices[0].message);
            res.status(200).send({ code: chatCompletion.choices[0].message })

        } catch (error) {
            res.status(500).json({ error: 'Internal Server Error' });
        }
    }
};

module.exports = CodeConverter

