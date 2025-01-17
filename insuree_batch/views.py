import os
from io import BytesIO

from django.http import FileResponse
from django.shortcuts import get_object_or_404, render

from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
import qrcode
import qrcode.image.svg

from . import services
from .apps import InsureeBatchConfig
from .models import InsureeBatch


def batch_qr(request):
    if not request.user.has_perms(InsureeBatchConfig.gql_query_batch_runs_perms):
        raise PermissionDenied(_("unauthorized"))
    batch_id = request.GET.get("batch")
    batch = get_object_or_404(InsureeBatch, id=batch_id)

    factory = qrcode.image.svg.SvgImage
    insuree_ids = []
    for item in batch.insuree_numbers.all():
        img = qrcode.make(item.insuree_number, image_factory=factory, box_size=10)
        stream = BytesIO()
        img.save(stream)
        insuree_ids.append({"insuree_number": item.insuree_number, "qr": stream.getvalue().decode()})

    return render(request, "insuree_batch/batch_qr.html", {"insuree_ids": insuree_ids, "batch": batch})


def export_insurees(request):
    if not request.user.has_perms(InsureeBatchConfig.gql_query_batch_runs_perms):
        raise PermissionDenied(_("unauthorized"))

    dry_run = request.GET.get("dryRun", "false").lower() == "true"
    batch_id = request.GET.get("batch")
    amount = request.GET.get("amount")

    if batch_id:
        batch = get_object_or_404(InsureeBatch, id=batch_id)
    else:
        batch = None

    zip_file = services.export_insurees(batch, amount, dry_run)
    response = FileResponse(open(zip_file.name, 'rb'), content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(zip_file.name)
    response['Content-Length'] = os.path.getsize(zip_file.name)
    return response
