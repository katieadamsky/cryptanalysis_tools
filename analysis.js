
/*
  Constructor for frequency distributions
*/
function frequency_dist(a, b, c, d, e, f, g, h, i, j, k, l, m, 
	n, o, p, q, r, s, t, u, v, w, x, y, z) {
	this['a'] = a || 0;
	this['b'] = b || 0;
	this['c'] = c || 0;
	this['d'] = d || 0;
	this['e'] = e || 0;
	this['f'] = f || 0;
	this['g'] = g || 0;
	this['h'] = h || 0;
	this['i'] = i || 0;
	this['j'] = j || 0;
	this['k'] = k || 0;
	this['l'] = l || 0;
	this['m'] = m || 0;
	this['n'] = n || 0;
	this['o'] = o || 0;
	this['p'] = p || 0;
	this['q'] = q || 0;
	this['r'] = r || 0;
	this['s'] = s || 0;
	this['t'] = t || 0;
	this['u'] = u || 0;
	this['v'] = v || 0;
	this['w'] = w || 0;
	this['x'] = x || 0;
	this['y'] = y || 0;
	this['z'] = z || 0;
}


function frequency_analysis(text) {
	// Find frequencies of the characters in the ciphertext
	var freq = new frequency_dist()
	// English frequency values from Wikipedia
	var english_freqs = new frequency_dist(
		8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,
		6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,
		0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074)
	var total = 0;
	for (var i=0; i<text.length; i++) {
		freq[text.charAt(i)]++;
		total++;
	}
	for (ch in freq) {
		freq[ch] /= parseFloat(total);
		freq[ch] *= 100;
	}

	/* 
	   Compare frequencies to those of common ciphers
	   First check: is it the same as regular English?
	   Calculate the correlation between english_freqs and freqs
	*/ 
	var transposition_corr = correlation(freq, english_freqs, Object.keys(freq), Object.keys(english_freqs))
	var results = "";
	results += "Correlation with regular English: " + Number(transposition_corr.toFixed(2)) + "\n"
	if (transposition_corr >= 0.8) {
		results += "<br>This could be a transposition cipher"
	}

	/*
		Is it a monoalphabetic substitution cipher?
		Sort the alphabet by descending frequency, then find the correlation
	*/
	sorted_english = Object.keys(english_freqs).sort(function(a, b){return english_freqs[b]-english_freqs[a]})
	sorted_cipher = Object.keys(freq).sort(function(a, b){return freq[b]-freq[a]})
	console.log(sorted_cipher)
	var monoalphabetic_corr = correlation(freq, english_freqs, sorted_cipher, sorted_english)
	results += "<br>Correlation between most frequent cipher letters and most frequent "
	 + "English letters: " + Number(monoalphabetic_corr.toFixed(2))
	if (monoalphabetic_corr >= 0.8) {
		results += "<br>This could be a <a href=\"monoalphabetic.html\">monoalphabetic substitution cipher</a>"
	}
	if (text.length % 2 == 0 && freq['j'] == 0) {
		results += "<br>Cipher contains an even number of letters and no J's"
		results += "<br>This could be a playfair cipher"
	}

	document.getElementById('results').innerHTML = results
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

function correlation(freqs_a, freqs_b, order_a, order_b) {
	var sumx = 0, sumy = 0, sumxy = 0, sumx2 = 0, sumy2 = 0;
	for (var i=0; i<26; i++) {
		var xi = freqs_a[order_a[i]]
		var yi = freqs_b[order_b[i]]
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
