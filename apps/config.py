from pathlib import Path

basedir = Path(__file__).parent.parent

# BaseConfigクラスを作成する
class BaseConfig:
    SECRET_KEY = "2AZSMss3p5QPbcY2hBsJ"
    WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"
    UPLOAD_FOLDER = str(Path(basedir, "apps", "images"))

    # BaseConfigクラスを作成する
        # 物体検知に利用するラベル
    LABELS = [
        "airplane",
        "apple",
        "banana",
        "baseball bat",
        "baseball glove",
        "bear",
        "bed",
        "bench",
        "bicycle",
        "bird",
        "boat",
        "book",
        "bottle",
        "bowl",
        "broccoli",
        "bus",
        "cake",
        "car",
        "carrot",
        "cell phone",
        "chair",
        "clock",
        "couch",
        "cow",
        "cup",
        "dining table",
        "dog",
        "door",
        "donut",
        "elephant",
        "eye glasses",
        "fire hydrant",
        "fork",
        "frisbee",
        "giraffe",
        "hair drier",
        "handbag",
        "hat",
        "hot dog",
        "horse",
        "keyboard",
        "kite",
        "knife",
        "laptop",
        "microwave",
        "mirror",
        "mouse",
        "orange",
        "oven",
        "parking meter",
        "person",
        "pizza",
        "potted plant",
        "refrigerator",
        "remote",
        "sandwich",
        "scissors",
        "sheep",
        "shoe",
        "skateboard",
        "skis",
        "snowboard",
        "spoon",
        "sports ball",
        "stop sign",
        "suitcase",
        "surfboard",
        "teddy bear",
        "tennis racket",
        "tie",
        "toaster",
        "toilet",
        "toothbrush",
        "traffic light",
        "train",
        "truck",
        "tv",
        "umbrella",
        "vase",
        "window",
        "wine glass",
        "zebra",
    ]


# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


# BaseConfigクラスを継承してTestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = str(Path(basedir, "tests", "detector", "images"))


# config辞書にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}
