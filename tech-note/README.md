## page
https://ny1030.github.io/pages/

## install list of my sphinx env.
```
brew install python3
pip install sphinx-rtd-theme
pip install sphinxcontrib-httpdomain
```

## how to build
```
make clean html
```

## how to release
```
cp -rp ./build/html/* ../docs/
```
