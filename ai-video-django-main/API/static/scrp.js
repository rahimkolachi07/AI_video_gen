const images = [
  'https://story21.s3.amazonaws.com/output/image/0.png',
  'https://story21.s3.amazonaws.com/output/image/1.png',
  'https://story21.s3.amazonaws.com/output/image/2.png',
  // Add more image URLs as needed
];

const audios = [
  'https://story21.s3.amazonaws.com/output/audio/0.mp3',
  'https://story21.s3.amazonaws.com/output/audio/1.mp3',
  'https://story21.s3.amazonaws.com/output/audio/2.mp3',
  // Add more audio URLs corresponding to each image
];

let currentIndex = 0;
let audioPlayer;
let isMuted = false;

const sliderImage = document.getElementById('sliderImage');
const imageText = document.getElementById('imageText');
sliderImage.src = images[currentIndex];

function playAudio() {
  if (!isMuted) {
    if (audioPlayer) {
      audioPlayer.pause();
    }
    audioPlayer = new Audio(audios[currentIndex]);
    audioPlayer.play();
  }
}

function changeSlide(direction) {
  currentIndex += direction;
  if (currentIndex < 0) {
    currentIndex = images.length - 1;
  } else if (currentIndex >= images.length) {
    currentIndex = 0;
  }
  sliderImage.src = images[currentIndex];
  displayText(); // Call displayText function after changing the image
  if (!isMuted) {
    playAudio();
  } else if (audioPlayer) {
    audioPlayer.pause();
  }
}

function toggleMute() {
  isMuted = !isMuted;
  const muteButton = document.getElementById('muteBtn');
  muteButton.textContent = isMuted ? 'Unmute' : 'Mute';
  if (isMuted && audioPlayer) {
    audioPlayer.pause();
  } else if (!isMuted && audioPlayer) {
    playAudio();
  }
}

function displayText() {
  // Fetch and parse the CSV file
  fetch('https://story21.s3.amazonaws.com/output/doc/paragraphs.csv')
    .then(response => response.text())
    .then(data => {
      const rows = data.split('\n'); // Split CSV into rows
      if (rows.length > currentIndex) {
        const text = rows[currentIndex].trim(); // Get the text for the current image
        imageText.textContent = text; // Display the text below the image
      }
    })
    .catch(error => {
      console.error('Error fetching or parsing CSV:', error);
    });
}
displayText(); // Call displayText function initially to display text for the first image
