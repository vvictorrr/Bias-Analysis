const vader = require('vader-sentiment');
const input = 'VADER is very smart, handsome, and funny';
const intensity = vader.SentimentIntensityAnalyzer.polarity_scores(input);
console.log(intensity);