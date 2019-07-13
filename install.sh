if [[ ! -e ./venv ]]; then
  python3.7 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
fi

cd static
npm install