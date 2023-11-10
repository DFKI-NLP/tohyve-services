// // import requests
// // import pyaudio

// // stream_url = "https://dfki-3109.dfki.de/stream"

// // # Fetch streaming data
// // response = requests.get(stream_url, stream=True)

// // # Initialize PyAudio
// // p = pyaudio.PyAudio()

// // # Open a streaming stream
// // stream = p.open(format=pyaudio.paInt16,
// //                 channels=1,
// //                 rate=44100,
// //                 output=True)

// // # Process streaming data
// // for chunk in response.iter_content(chunk_size=1024):
// //     if chunk:
// //         # Process the audio chunk (decode, analyze, etc.) if necessary
// //         # Here, we'll just play the audio chunk
// //         stream.write(chunk)

// // # Close the stream and PyAudio
// // stream.stop_stream()
// // stream.close()
// // p.terminate()
// ////////////////////////////////////////////////////////////////////////////////////////////////
// // const axios = require('axios');
// // const fs = require('fs');
// // const streamUrl = 'https://dfki-3109.dfki.de/stream';

// // axios({
// //   method: 'get',
// //   url: streamUrl,
// //   responseType: 'stream'
// // })
// //   .then(response => {
// //     const audioFileStream = fs.createWriteStream('streamed_audio.mp3'); // Save audio as 'streamed_audio.mp3'

// //     // Pipe the streaming data to the file stream
// //     response.data.pipe(audioFileStream);

// //     // Handle stream end event (when all data has been received)
// //     response.data.on('end', () => {
// //       console.log('Streaming data saved successfully.');
// //     });

// //     // Handle errors
// //     response.data.on('error', err => {
// //       console.error('Error streaming audio:', err);
// //     });
// //   })
// //   .catch(error => {
// //     console.error('Error fetching streaming data:', error);
// //   });
// ////////////////////////////////////////////////////////////////////////////////////////////////



// const axios = require('axios');
// const WebSocket = require('websocket').client;

// const streamUrl = 'https://dfki-3109.dfki.de/stream'; // need to change it with the input value
// const websocketServerUrl = 'wss://dfki-3109.dfki.de/ws';

// const socket = new WebSocket(websocketServerUrl);

// axios({
//   method: 'get',
//   url: streamUrl,
//   responseType: 'stream'
// })
//   .then(response => {
//     // Handle incoming audio data
//     response.data.on('data', chunk => {
//       // Concatenate audio chunks into a single Buffer
//       const audioBuffer = Buffer.concat(chunk);

//       // Convert audio buffer to base64
//       const audioBase64 = audioBuffer.toString('base64');
  
//       // Format the data into a JSON object
//       const jsonData = {
//         fn_index:4,
//         data:[
//             "de",
//             {
//                 data:audioBase64,
//                 name:"audio.mp3"
//             }
//         ],
//         target_language:"en"
//       };
//       console.log(jsonData);
//       if (socket.readyState === WebSocket.OPEN) {
//         // Send audio data as base64 to WebSocket server
//         socket.send(JSON.stringify(jsonData));
//       }

//     });

//     // Handle stream end event (when all data has been received)
//     response.data.on('end', () => {
//       console.log('Stopped streaming!!');
//     });

//     // Handle errors
//     response.data.on('error', err => {
//       console.error('Error streaming audio:', err);
//     });
//   })
//   .catch(error => {
//     console.error('Error fetching streaming data:', error);
//   });

// // Event handler for socket connection
// socket.on('connect', connection => {
//   console.log('Connected to WebSocket server.');
// });

// // Event handler for socket incoming messages
// socket.onmessage = (event) => {
//   // Parse the JSON response
//   var jsonResponse = JSON.parse(event.data);

//   var keys = Object.keys(jsonResponse);
//   // Iterate over the keys and log them
//   keys.forEach(function (key) {
//       if (key == "asr"){
//           var row = table.insertRow();
//           console.log('key Response:', jsonResponse[key]);
//           var asr_cell = row.insertCell(0);
//           asr_cell.innerHTML = jsonResponse[key];
//       }
//       if (key == "mt"){
//           var row = table.insertRow();
//           console.log('key Response:', jsonResponse[key]);
//           var mt_cell = row.insertCell(0);
//           mt_cell.innerHTML = jsonResponse[key];
//       }
//       if (key == "tts"){
//           var row = table.insertRow();
//           console.log('key Response:', jsonResponse[key]);
//           var tts_cell = row.insertCell(0);
//           tts_cell.innerHTML = jsonResponse[key];
//       }
//       if (key == "audio"){
//           const binaryAudioData = atob(jsonResponse["audio"]);
//           // Create a Uint8Array from the binary data
//           const uint8Array = new Uint8Array(binaryAudioData.length);
//           for (let i = 0; i < binaryAudioData.length; i++) {
//               uint8Array[i] = binaryAudioData.charCodeAt(i);
//           }
//           const outputAudioBlob = new Blob([uint8Array], { type: 'audio/wav' });
//           // Set the audio element's source to the recorded audio
//           audioPlayer.src = URL.createObjectURL(outputAudioBlob);
//       }
//   });
//   // Create a new table row for the separator
//   var separatorRow = document.createElement("tr");

//   // Create separator cell
//   var separatorCell = document.createElement("td");
//   separatorCell.colSpan = 2; // Span across two columns
//   separatorCell.textContent = "---------------------------------------------------------------";

//   // Append the separator cell to the separator row
//   separatorRow.appendChild(separatorCell);

//   // Append the separator row to the table
//   table.appendChild(separatorRow);
// };

// // Event handler on socket close
// socket.onclose = (event) => {
//   if (event.wasClean) {
//       console.log('Closed cleanly, code=${event.code}, reason=${event.reason}');
//   } else {
//       console.error('Connection died');
//   }
// };



