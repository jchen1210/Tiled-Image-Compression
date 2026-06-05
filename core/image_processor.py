from skimage import filters
from PIL import Image
from .config import ImageSettings
import numpy as np

NUM_COLOURS = 10

class ImageData:
    '''
    Computes and houses image data necessary for creating a tiling of the image
    '''
    def __init__(self, img, settings: ImageSettings):
        self.settings = settings

        num_rows = settings.num_rows
        num_cols = settings.num_cols
        block_size = settings.block_size

        img = img.convert("L")
        img = img.resize((num_cols*block_size, num_rows*block_size), Image.LANCZOS) # type: ignore
        self.img_arr = np.array(img)
        self._laplacian = None
        self._brightnesses = None

    @property
    def laplacian(self):
        if self._laplacian is None:
            num_rows = self.num_rows
            num_cols = self.num_cols
            block_size = self.settings.block_size

            laplace_edges = filters.laplace(self.img_arr / 255.0)

            edge_block = np.zeros((num_rows, num_cols))
            for i in range(num_rows):
                for j in range(num_cols):
                    block = laplace_edges[i*block_size:(i+1)*block_size,
                                        j*block_size:(j+1)*block_size]
                    edge_block[i,j] = np.mean(np.abs(block))

            edge_block /= np.max(edge_block)
            edge_block = np.clip(edge_block, 0, 1)

            self._laplacian = edge_block
            return self._laplacian
        else:
            return self._laplacian

    @property
    def brightnesses(self):
        if self._brightnesses is None:
            num_rows = self.num_rows
            num_cols = self.num_cols
            block_size = self.settings.block_size

            brightness_arr = np.zeros((num_rows, num_cols))
            for i in range(num_rows):
                for j in range(num_cols):
                    block = self.img_arr[i*block_size:(i+1)*block_size,
                                        j*block_size:(j+1)*block_size]
                    brightness_arr[i,j] = round(block.mean() / 255.0 * (NUM_COLOURS - 1))
            
            self._brightnesses = brightness_arr
            return brightness_arr
        else:
            return self._brightnesses
    
    @property
    def num_rows(self):
        return self.settings.num_rows
    
    @property
    def num_cols(self):
        return self.settings.num_cols


class Palette:
    '''
    A colour palette used for tiling the image
    '''
    def __init__(self, colours: list[tuple]):
        self.colours = colours
        self.num_colours = len(colours)

    def colour_to_brightness(self):
        brightness_values = []
        for (r, g, b) in self.colours:
            brightness = 0.299*r + 0.587*g + 0.114*b
            brightness_values.append(brightness)

        brightness_values = np.array(brightness_values)
        normalized_brightness = (brightness_values - brightness_values.min()) / \
                            (brightness_values.max() - brightness_values.min()) * 9
        self.colour_to_brightness_dict = dict(zip(self.colours, normalized_brightness))
        return self.colour_to_brightness_dict