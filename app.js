const express = require('express');
const bodyParser = require('body-parser');
const { openai } = require('openai');
require('dotenv').config();
const CodeConverter = require('./routes/codeConverter');
const CodeDebuger = require('./routes/debug');
const CodeQualityChecker = require('./routes/quality_checker');
const app = express();
var cors = require('cors');

const session = require('express-session');
const passport = require('passport');
const GitHubStrategy = require('passport-github').Strategy;
const { v4: uuidv4 } = require('uuid');

// const sessionSecret = uuidv4();
// console.log(sessionSecret);

app.use(bodyParser.json());
const corsOptions = {
  origin: 'http://localhost:3000', // Replace with your frontend's port
};
app.use(cors(corsOptions));

app.use(session({ secret: process.env.SESSION_SECRET, resave: true, saveUninitialized: true }));
app.use(passport.initialize());
app.use(passport.session());

// Define routes

app.get('/',(req,res)=>{
    res.send('Code converter api ')
})

app.post('/code-converter', CodeConverter);

app.post('/debug',CodeDebuger);

app.post('/quality-check', CodeQualityChecker);

passport.use(new GitHubStrategy({
  clientID: process.env.GITHUB_CLIENT_ID,
  clientSecret: process.env.GITHUB_CLIENT_SECRET,
  callbackURL: process.env.CALLBACK_URL
}, (accessToken, refreshToken, profile, done) => {
  // Store user data in session or database
  return done(null, profile);
}));

passport.serializeUser((user, done) => {
  done(null, user);
});

passport.deserializeUser((user, done) => {
  done(null, user);
});

app.get('/auth/github/callback',
  passport.authenticate('github', { failureRedirect: '/' }),
  (req, res) => {
    res.redirect('/'); // Redirect to the dashboard or code conversion page
  }
);

router.get('/getAccessToken', async (req, res) => {
  try {
    const { code } = req.body;
    const response = await axios.post(`https://github.com/login/oauth/access_token`, null, {
      params: {
        client_id: process.env.GITHUB_CLIENT_ID,
        client_secret: process.env.GITHUB_CLIENT_SECRET,
        code: code,
        redirect_uri: process.env.redirect_uri,
      },
      headers: {
        Accept: 'application/json'
      }
    });

    const accessToken = response.data.access_token;
    res.json({ accessToken });
  } catch (error) {
    console.error('Error exchanging code for access token:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Start the server
app.listen(8080, () => {
  console.log(`Server is running on http://localhost:${8080}`);
});
