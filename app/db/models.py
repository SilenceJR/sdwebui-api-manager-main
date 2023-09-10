from pydantic import BaseModel
from typing import List, Optional, Any

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Img2imgArgs(BaseModel):
    init_images: Optional[List[str]]
    resize_mode: Optional[int]
    denoising_strength: Optional[float]
    image_cfg_scale: Optional[int]
    mask: Optional[str]
    mask_blur: Optional[int]
    inpainting_fill: Optional[int]
    inpaint_full_res: Optional[bool]
    inpaint_full_res_padding: Optional[int]
    inpainting_mask_invert: Optional[bool]
    initial_noise_multiplier: Optional[int]
    prompt: Optional[str]
    styles: Optional[List[str]]
    seed: Optional[int]
    subseed: Optional[int]
    subseed_strength: Optional[int]
    seed_resize_from_h: Optional[int]
    seed_resize_from_w: Optional[int]
    sampler_name: Optional[str]
    batch_size: Optional[int]
    n_iter: Optional[int]
    steps: Optional[int]
    cfg_scale: Optional[int]
    width: Optional[int]
    height: Optional[int]
    restore_faces: Optional[bool]
    tiling: Optional[bool]
    do_not_save_samples: Optional[bool]
    do_not_save_grid: Optional[bool]
    negative_prompt: Optional[str]
    eta: Optional[int]
    s_min_uncond: Optional[int]
    s_churn: Optional[int]
    s_tmax: Optional[int]
    s_tmin: Optional[int]
    s_noise: Optional[int]
    override_settings: Optional[dict]
    override_settings_restore_afterwards: Optional[bool]
    script_args: Optional[List[dict]]
    sampler_index: Optional[str]
    include_init_images: Optional[bool]
    script_name: Optional[str]
    send_images: Optional[bool]
    save_images: Optional[bool]
    alwayson_scripts: Optional[dict]
    options: Optional[dict]


class Txt2imgArgs(BaseModel):
    enable_hr: Optional[bool]
    denoising_strength: Optional[float]
    firstphase_width: Optional[int]
    firstphase_height: Optional[int]
    hr_scale: Optional[int]
    hr_upscaler: Optional[str]
    hr_second_pass_steps: Optional[int]
    hr_resize_x: Optional[int]
    hr_resize_y: Optional[int]
    prompt: Optional[str]
    styles: Optional[List[str]]
    seed: Optional[int]
    subseed: Optional[int]
    subseed_strength: Optional[int]
    seed_resize_from_h: Optional[int]
    seed_resize_from_w: Optional[int]
    sampler_name: Optional[str]
    batch_size: Optional[int]
    n_iter: Optional[int]
    steps: Optional[int]
    cfg_scale: Optional[int]
    width: Optional[int]
    height: Optional[int]
    restore_faces: Optional[bool]
    tiling: Optional[bool]
    do_not_save_samples: Optional[bool]
    do_not_save_grid: Optional[bool]
    negative_prompt: Optional[str]
    eta: Optional[int]
    s_min_uncond: Optional[int]
    s_churn: Optional[int]
    s_tmax: Optional[int]
    s_tmin: Optional[int]
    s_noise: Optional[int]
    override_settings: Optional[dict]
    override_settings_restore_afterwards: Optional[bool]
    script_args: Optional[List[dict]]
    sampler_index: Optional[str]
    script_name: Optional[str]
    send_images: Optional[bool]
    save_image: Optional[bool]
    alwayson_scripts: Optional[dict]
    options: Optional[dict]


class ExtraSingleImage(BaseModel):
    resize_mode: Optional[int]
    show_extras_results: Optional[bool]
    gfpgan_visibility: Optional[int]
    codeformer_visibility: Optional[int]
    codeformer_weight: Optional[float]
    upscaling_resize: Optional[int]
    upscaling_resize_w: Optional[int]
    upscaling_resize_h: Optional[int]
    upscaling_crop: Optional[bool]
    upscaler_1: Optional[str]
    upscaler_2: Optional[str]
    extras_upscaler_2_visibility: Optional[int]
    upscale_first: Optional[bool]
    image: Optional[str]


class ResponseModel:
    code: Optional[int]
    data: Optional[any]
    msg: Optional[str]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    prompt = Column(String, index=True)
    reply = Column(String, index=True)
    req_id = Column(String, index=True)


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True,index=True)
    description = Column(String)
    req_id = Column(String)
    image = Column(String)
