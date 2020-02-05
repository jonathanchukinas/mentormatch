from mentormatch.importer import ImporterFactory


def test_import(test_files_dir, home_dir):
    test_file_path = test_files_dir / 'applications.xlsx'
    exporter_factory = ImporterFactory
    importer = exporter_factory.get_excel_importer(
        source_path=test_file_path,
    )
    importer.execute()




#
# def test_toml(test_files_dir):
#     import toml
#     _d = {
#         'happy': 'a',
#         'fdsafdsa': 'b',
#     }
#
#     path = test_files_dir / 'myfile.toml'
#     path.write_text(toml.dumps(_d))
