# Shadebags
 Shade is an extremely fast & highly queryable bag format built for big data robotics. Compress &amp; query ROS or custom data.

## Features

* Highly modular, adding new compression algorithms and bag types is easy
* Multicore compression - compress extremely fast (we experienced a 5x speed boost over `rosbag compress`)
* Better compression ratios. By matching the algorithm to the datatype, much better compression ratios are achieved

## Usage

Just `pip install shadebags` and `shadebags compress ./example.bag ROS1`

This will give a new file `./example.shade`. To recover the original bag just run

`shadebags decompress ./example.shade`.

