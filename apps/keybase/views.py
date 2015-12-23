# -*- coding: utf-8 -*-
from django.shortcuts import render


def proof(request):
    return render(request, 'tpl/keybase/proof.txt', content_type='text/plaintext')
