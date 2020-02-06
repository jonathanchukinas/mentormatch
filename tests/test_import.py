from mentormatch.importer import ImporterFactory
import names
import toml


def test_import(test_files_dir, home_dir):
    test_file_path = test_files_dir / 'applications.xlsx'
    exporter_factory = ImporterFactory
    importer = exporter_factory.get_excel_importer(
        source_path=test_file_path,
    )
    importer.execute()


# def test_generate_names(test_files_dir):
#
#     # Generate Names
#     name_count = 200
#     _names = {}
#     for gender in 'male female'.split():
#         _names[f'first_names_{gender}'] = [
#             names.get_first_name(gender=gender)
#             for _ in range(name_count)
#         ]
#     _names['last_names'] = [
#         names.get_last_name()
#         for _ in range(name_count * 2)
#     ]
#
#     # Save to file
#     test_file_path = test_files_dir / 'names.toml'
#     test_file_path.write_text(toml.dumps(_names))


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
