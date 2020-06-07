## page
https://ny1030.github.io/pages/

## install list of my sphinx env.
```
brew install python3
pip install sphinx-rtd-theme
pip install sphinxcontrib-httpdomain
```

## how to build
- tech-note/で以下を実行
```
make clean html
```

## how to release
- tech-note/で以下を実行
```
cp -rp ./build/html/* ../docs/
```
