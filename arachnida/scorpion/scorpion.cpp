#include <iostream>
#include <exiv2/exiv2.hpp>

int main(int argc, char* argv[])
{
	if (argc < 2) {
		std::cerr << "Usage: " << argv[0] << " image-file\n";
		return 1;
	}
	try {
		Exiv2::Image::AutoPtr image = Exiv2::ImageFactory::open(argv[1]);
		if (image.get() == 0) {
			std::cerr << "File format not supported: " << argv[1] << std::endl;
			return 1;
		}
		image->readMetadata();
		Exiv2::ExifData& exifData = image->exifData();
		if (!exifData.empty()) {
			std::cout << "Exif data:\n";
			for (Exiv2::ExifData::const_iterator it = exifData.begin(); it != exifData.end(); ++it) {
				std::cout << it->key() << ": " << it->value() << "\n";
			}
		}
		Exiv2::IptcData& iptcData = image->iptcData();
		if (!iptcData.empty()) {
			std::cout << "IPTC data:\n";
			for (Exiv2::IptcData::const_iterator it = iptcData.begin(); it != iptcData.end(); ++it) {
				std::cout << it->key() << ": " << it->value() << "\n";
			}
		}
		Exiv2::XmpData& xmpData = image->xmpData();
		if (!xmpData.empty()) {
			std::cout << "XMP data:\n";
			for (Exiv2::XmpData::const_iterator it = xmpData.begin(); it != xmpData.end(); ++it) {
				std::cout << it->key() << ": " << it->value() << "\n";
			}
		}
	}
	catch (std::exception& e) {
		std::cerr << "Error: " << e.what() << "\n";
		return 1;
	}
	return 0;
}
