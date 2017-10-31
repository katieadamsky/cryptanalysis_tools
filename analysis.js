var english_freqs = {
	'a':8.167,'b':1.492,'c':2.782,'d':4.253,'e':12.702,'f':2.228,'g':2.015,
	'h':6.094,'i':6.966,'j':0.153,'k':0.772,'l':4.025,'m':2.406,'n':6.749,'o':7.507,'p':1.929,
	'q':0.095,'r':5.987,'s':6.327,'t':9.056,'u':2.758,'v':0.978,'w':2.360,'x':0.150,'y':1.974,'z':0.074
}

function frequency_analysis(text) {
	// Find frequencies of the characters in the ciphertext
	var freq = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,
	'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,
	'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0};
	var total = 0;
	for (var i=0; i<text.length; i++) {
		freq[text.charAt(i)]++;
		total++;
	}
	for (ch in freq) {
		freq[ch] /= parseFloat(total);
		freq[ch] *= 100;
	}
	console.log(freq);

	/* 
	   Compare frequencies to those of common ciphers
	   First check: is it the same as regular English?
	   Calculate the correlation between english_freqs and freqs
	*/ 
	var corr = correlation(freq, english_freqs)
	var results = "";
	results += "Correlation with regular English: " + Number(corr.toFixed(2)) + "%\n"
	if (corr >= 0.8) {
		results += "<br>This could be a transposition cipher"
	}

	document.getElementById('results').innerHTML = results
	/*
		Is it a monoalphabetic substitution cipher?
		Sort the alphabet by descending frequency, then find the correlation
	*/
	var corr2 = correlation()

	return freq;
}

function analysis(form) {
	var freq = frequency_analysis(form.ciphertext.value.toLowerCase());
	var nums = Object.entries(freq).map(([key, value]) => {
	  return value;
	})
	new Chart(document.getElementById("chart"), {
    type: 'bar',
    data: {
      labels: Object.keys(freq),
      datasets: [
        {
          label: "Frequency",
          data: nums
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Frequency Analysis',
        fontSize: 24
      }
    }
    });
}

function correlation(freqs_a, freqs_b) {
	var sumx = 0, sumy = 0, sumxy = 0, sumx2 = 0, sumy2 = 0;
	// for (ch in freqs_a) {
	for (var i=0; i<26; i++) {
		var xi = freqs_a[Object.keys(freqs_a)[i]]
		var yi = freqs_b[Object.keys(freqs_b)[i]]
		sumx += xi;
		sumy += yi;
		sumxy += xi * yi;
		sumx2 += Math.pow(xi, 2);
		sumy2 += Math.pow(yi, 2);
	}
	return (26 * sumxy - sumx * sumy) 
	/ (Math.sqrt(26*sumx2 - Math.pow(sumx, 2)) 
	* Math.sqrt(26 * sumy2 - Math.pow(sumy, 2)));
}
