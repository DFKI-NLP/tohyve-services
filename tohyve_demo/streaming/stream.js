// import requests
// import pyaudio

// stream_url = "https://dfki-3109.dfki.de/stream"

// # Fetch streaming data
// response = requests.get(stream_url, stream=True)

// # Initialize PyAudio
// p = pyaudio.PyAudio()

// # Open a streaming stream
// stream = p.open(format=pyaudio.paInt16,
//                 channels=1,
//                 rate=44100,
//                 output=True)

// # Process streaming data
// for chunk in response.iter_content(chunk_size=1024):
//     if chunk:
//         # Process the audio chunk (decode, analyze, etc.) if necessary
//         # Here, we'll just play the audio chunk
//         stream.write(chunk)

// # Close the stream and PyAudio
// stream.stop_stream()
// stream.close()
// p.terminate()
////////////////////////////////////////////////////////////////////////////////////////////////
// const axios = require('axios');
// const fs = require('fs');
// const streamUrl = 'https://dfki-3109.dfki.de/stream';

// axios({
//   method: 'get',
//   url: streamUrl,
//   responseType: 'stream'
// })
//   .then(response => {
//     const audioFileStream = fs.createWriteStream('streamed_audio.mp3'); // Save audio as 'streamed_audio.mp3'

//     // Pipe the streaming data to the file stream
//     response.data.pipe(audioFileStream);

//     // Handle stream end event (when all data has been received)
//     response.data.on('end', () => {
//       console.log('Streaming data saved successfully.');
//     });

//     // Handle errors
//     response.data.on('error', err => {
//       console.error('Error streaming audio:', err);
//     });
//   })
//   .catch(error => {
//     console.error('Error fetching streaming data:', error);
//   });
////////////////////////////////////////////////////////////////////////////////////////////////



const axios = require('axios');
const streamUrl = 'https://dfki-3109.dfki.de/stream';
const socketIOClient = require('socket.io-client');
const socket = socketIOClient('http://your-socket-server-address'); // Replace with your socket server address

axios({
  method: 'get',
  url: streamUrl,
  responseType: 'stream'
})
  .then(response => {
    // Create a buffer to store audio chunks
    const audioChunks = [];

    // Handle incoming audio data
    response.data.on('data', chunk => {
      audioChunks.push(chunk);
    });

    // Handle stream end event (when all data has been received)
    response.data.on('end', () => {
      // Concatenate audio chunks into a single buffer
      const audioBuffer = Buffer.concat(audioChunks);

      // Convert audio buffer to base64
      const audioBase64 = audioBuffer.toString('base64');

      // Send base64 audio data over the socket
      socket.emit('audio', audioBase64);

      console.log('Streaming data sent successfully.');
    });

    // Handle errors
    response.data.on('error', err => {
      console.error('Error streaming audio:', err);
    });
  })
  .catch(error => {
    console.error('Error fetching streaming data:', error);
  });
