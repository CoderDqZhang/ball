#!/usr/bin/env python
# -*- coding: utf-8 -*-


from enum import IntEnum, unique


@unique
class ErrorsEnum(IntEnum):
    INVITATION_CODE_NON_EXIST = 200014

    def describe(self):
        return _ERRORS.get(self)

_ERRORS = {
    ErrorsEnum.INDUSTRY_NAME_REQUIRED: u"请输入行业名称",
    ErrorsEnum.INDUSTRY_NAME_EXISTS: u"已存在相同行业",

    ErrorsEnum.USER_NAME_REQUIRED: u"请输入用户名",
    ErrorsEnum.USER_NAME_EXISTS: u"已存在相同用户名",
    ErrorsEnum.USER_SOCIAL_ID_EXISTS: u"已存在相同OPENID",

    ErrorsEnum.HEIGHT_ERROR: u"身高输入错误",
    ErrorsEnum.LOCATION_ERROR: u"所在地输入错误",
    ErrorsEnum.HOMETOWN_ERROR: u"家乡输入错误",

    ErrorsEnum.IMAGE_ERROR: u"图片格式错误",
    ErrorsEnum.PHOTO_REQUIRED: u"请选择要上传的照片",
    ErrorsEnum.INVITATION_TYPE_REQUIRED: u"请选择邀约类型",
    # TODO 提示信息
    ErrorsEnum.INVITATION_CODE_REQUIRED: u"邀请码缺失",
    ErrorsEnum.SOCIAL_ID_REQUIRED: u"SOCIAL_ID缺失",
    ErrorsEnum.INVITATION_CODE_INVALID: u'邀请码已过期',
    ErrorsEnum.INVITATION_CODE_NON_EXIST: u'邀请码不存在',
}