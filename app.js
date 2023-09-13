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
app.use(cors())

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

app.get('/repos', (req, res) => {
  const accessToken = req.user.accessToken;
  axios.get('https://api.github.com/user/repos', {
      headers: {
          Authorization: `Bearer ${accessToken}`
      }
  })
  .then(response => {
      res.json(response.data);
  })
  .catch(error => {
      res.status(500).send('Error fetching repositories');
  });
  
});

// Start the server
app.listen(8080, () => {
  console.log(`Server is running on http://localhost:${8080}`);
});
