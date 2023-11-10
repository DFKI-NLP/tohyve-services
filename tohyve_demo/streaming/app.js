const express = require('express');
const http = require('http');
const cors = require('cors');
const socketIo = require('socket.io');
const fluentFfmpeg = require('fluent-ffmpeg');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);


const corsOptions = {
  origin: '*',
  exposedHeaders: ['Content-Length', 'Authorization'],
  methods: 'GET,PUT,POST,DELETE',
  optionsSuccessStatus: 204,
};

app.use(cors(corsOptions));

const port = process.env.PORT || 8080;

server.listen(port, () => {
  console.log('Server is running on http://localhost:${port}');
});

 // Add more audio files as needed
const audioFilePaths = [];
for(let i = 1; i<11; i++){
  audioFilePaths.push("/usr/src/app/audios/audio_"+i+".mp3");
}

let currentAudioIndex = 0;

// Serve the audio stream
app.get('/stream', (req, res) => {
  const currentAudioFilePath = audioFilePaths[currentAudioIndex];

  const ffmpegCommand = fluentFfmpeg(currentAudioFilePath)
      .format('mp3')
      .on('error', (err) => {
          console.error('FFmpeg error:', err);
        })
      .on('end', () => {
      console.log('Streaming finished');
      })
      .on('close', (code, signal) => {
          console.log(`FFmpeg process closed with code ${code} and signal ${signal}`);
      })
      .pipe(res, { end: true });

    currentAudioIndex = (currentAudioIndex + 1) % audioFilePaths.length; // Cycle through audio files
    if(currentAudioIndex > 9){
      currentAudioIndex = 0;
    }
});

// Broadcast the audio stream to connected clients
io.on('connection', (socket) => {
    console.log('Client connected');
    socket.on('disconnect', () => {
        console.log('Client disconnected');
        // You may add additional handling when a client disconnects
        if (ffmpegProcess) {
            ffmpegProcess.kill(); // Stop the FFmpeg process on client disconnect
        }
    });
});

// Send audio data to clients
setInterval(() => {
  io.emit('audio', '/stream');
}, 1000);
