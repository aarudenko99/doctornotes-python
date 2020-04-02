from django.contrib import admin

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.admin import ImportExportModelAdmin

from .models import Category, Tag, Type, Macro, Note


class MacroResource(resources.ModelResource):

    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     dataset.insert_col(0, col=["", ] * dataset.height, header="id")
    #
    # def get_instance(self, instance_loader, row):
    #     return False

    Type = fields.Field(
        column_name='Type',
        attribute='Type',
        widget=ForeignKeyWidget(Type, 'title'))

    Tags = fields.Field(
        column_name='Tags',
        attribute='Tags',
        widget=ManyToManyWidget(Tag, field='title'))

    Category = fields.Field(
        column_name='Category',
        attribute='Category',
        widget=ForeignKeyWidget(Category, 'title'))

    class Meta:
        model = Macro
        skip_unchanged = True
        report_skipped = True
        exclude = ('id', )
        import_id_fields = ('Title',)

        fields = ('Type', 'Tags', 'Category', 'Abbreviation', 'Title', 'Content')


@admin.register(Macro)
class MacroAdmin(ImportExportModelAdmin):
    resource_class = MacroResource
    list_display = ('id', 'Type', 'tags_list', 'Category', 'Abbreviation', 'Title', 'Content')
    search_fields = ('Title', 'Category__title', 'Type__title', 'Abbreviation', 'Content', )

    def tags_list(self, obj):
        tags = [t.title for t in obj.Tags.all()]
        return ','.join(tags) if tags else '-'



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

    def __str__(self):
        return self.title


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')