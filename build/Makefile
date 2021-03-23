.PHONY: buildImageAmd64 buildImageArm64 restart

buildImageAmd64:
	docker build -f ./dockerfile-sum/amd64 --tag video-download-rtsp-amd64:1.0 .

buildImageArm64:
	docker build -f ./dockerfile-sum/arm64 --tag video-download-rtsp-arm64:1.0 .
	docker build -f ./dockerfile-sum/arm64 --tag video-download-rtsp-dns-arm64:1.0 .
