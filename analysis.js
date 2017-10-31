

function frequency_analysis(text) {
	var freq = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,
	'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,
	'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0};
	for (var i=0; i<text.length; i++) {
		freq[text.charAt(i)]++;
	}
	console.log(freq);
	return freq;
}

function analysis(form) {
	console.log(form.ciphertext.value)
	var freq = frequency_analysis(form.ciphertext.value.toLowerCase());
	var nums = Object.entries(freq).map(([key, value]) => {
	  return value;
	})
	console.log(nums);
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