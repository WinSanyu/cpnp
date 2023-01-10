import torch
import logging
import os.path
import sys
sys.path.append("..") 

from utils import utils_option as option
from utils import utils_image as util
from utils import utils_logger

# from data.select_dataset import define_Dataset
from models.select_network import define_G

def gen_logger(opt):
    util.mkdirs((path for key, path in opt['path'].items() if 'pretrained' not in key))
    logger_name = 'pnp'
    utils_logger.logger_info(logger_name, os.path.join(opt['path']['log'], logger_name+'.log'))
    logger = logging.getLogger(logger_name)
    return logger

def get_opt(json_path):
    opt = option.parse(json_path, is_train=False)
    opt = option.dict_to_nonedict(opt)
    return opt

def get_network_eval(opt):
    model = define_G(opt)
    model_path = opt['pnp']['denoisor_pth'] # opt['path']['pretrained_netG']
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    for k, v in model.named_parameters():
        v.requires_grad = False
    return model

def save_opt(opt, pth='sndncnn.json'):
    import json
    with open(pth, 'w') as f:
        json.dump(opt, f)


# def get_test_loader(opt):
#     dataset_opt = opt['datasets']['test']
#     dataset_opt['sigma_test'] = opt['sigma_test']
#     test_set = define_Dataset(dataset_opt)
#     test_loader = DataLoader(test_set, batch_size=1,
#                              shuffle=False, num_workers=1,
#                              drop_last=False, pin_memory=True)
#     return test_loader