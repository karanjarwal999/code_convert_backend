const express = require('express');
const bodyParser = require('body-parser');
const { openai } = require('openai');
require('dotenv').config();
var cors = require('cors');
const CodeConverter = require('./routes/codeConverter');
const CodeDebuger = require('./routes/debug');
const CodeQualityChecker = require('./routes/quality_checker');
const app = express();

app.use(bodyParser.json());
app.use(cors())


// Define routes
app.get('/',(req,res)=>{
    res.send('Code converter api ')
})

app.post('/code-converter', CodeConverter);

app.post('/debug',CodeDebuger);

app.post('/quality-check', CodeQualityChecker);

// Start the server
app.listen(8080, () => {
  console.log(`Server is running on http://localhost:${8080}`);
});
