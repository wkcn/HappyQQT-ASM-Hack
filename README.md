# HappyQQT-ASM Hack
Learn to **modify** the memory of [HappyQQT-ASM](https://github.com/wkcn/HappyQQT-ASM) on Linux

## Usage

### Build HappyQQT-ASM
```
git clone https://github.com/wkcn/HappyQQT-ASM
cd HappyQQT-ASM
make
```

### Deploy HappyQQT-ASM Hack
```
git clone https://github.com/wkcn/HappyQQT-ASM-Hack
cd HappyQQT-ASM-Hack
```

Make soft links of `HappyQQT-ASM/main` and `HappyQQT/game`

The files in the directory:
```
.
├── game -> ../HappyQQT-ASM/game
├── hack.py
├── main -> ../HappyQQT-ASM/main
├── README.md
└── res
    ├── BGM
    │   └── bomb.ogg
    └── SE
        └── X10_01.wav
```

Run the hack program:
```
python3 hack.py
```
