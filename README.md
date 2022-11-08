# Option Valuation with Python

An option valuation webapp in Python.

### Models

- [Binomial (Cox, Ross & Rubinstein)](https://github.com/romaincaraes/option-valuation-python/blob/master/option-valuation/models/binomial.py),
- [Black & Scholes](https://github.com/romaincaraes/option-valuation-python/blob/master/option-valuation/models/blackscholes.py),
- [Monte Carlo](https://github.com/romaincaraes/option-valuation-python/blob/master/option-valuation/models/montecarlo.py)


### Installation

Clone this repository :

	git clone https://github.com/romaincaraes/option-valuation-python
	cd option-valuation-python
	
You may want to use a virtual environment to keep a clean Python installation :

	python3 -m venv venv/
	source venv/bin/activate

Install the required dependencies :

	pip3 install -r requirements.txt
	
### Usage

To use the Option Valuation web app, run the __option.py__ script in __option-valuation/__ folder : 

	cd option-valuation
	streamlit run option.py

A new tab should open in your browser :

![Streamlit Web App Screenshot](img/screenshot.png)

### Built With

- [Numpy](https://numpy.org/) - Fundamental package for scientific computing with Python,
- [Pandas](https://pandas.pydata.org/) - Library providing data structures and data analysis tools for Python,
- [Scipy](https://scipy.org/) - Software for mathematics, science, and engineering,
- [Streamlit](https://streamlit.io) - Open-source app framework,

### Dependencies

All the Python packages needed are listed in [requirements.txt](https://github.com/romaincaraes/option-valuation-python/blob/master/requirements.txt) and on the [Dependency Graph page](https://github.com/romaincaraes/option-valuation-python/network/dependencies).


### License

This project is licensed under the [MIT License](https://github.com/romaincaraes/option-valuation-python/blob/master/LICENSE).


### Authors

- **Romain Caraës** - [romaincaraes](https://github.com/romaincaraes)

See also the [GitHub Contributors page](https://github.com/romaincaraes/option-valuation-python/graphs/contributors).
