const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const fluentFfmpeg = require('fluent-ffmpeg');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Serve static files from the 'public' directory
app.use(express.static('public'));

const port = process.env.PORT || 3000;

server.listen(port, () => {
  console.log('Server is running on http://localhost:${port}');
});

const audioFilePath = 'audio.mp3';

// Serve the audio stream
app.get('/stream', (req, res) => {
    const ffmpegCommand = fluentFfmpeg(audioFilePath)
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
});

// Broadcast the audio stream to connected clients
io.on('connection', (socket) => {
    console.log('Client connected');
    socket.on('disconnect', () => {
        console.log('Client disconnected');
        if (ffmpegProcess) {
            ffmpegProcess.kill(); // Stop the FFmpeg process on client disconnect
        }
    });
});

// Send audio data to clients
setInterval(() => {
  io.emit('audio', '/stream');
}, 1000);
