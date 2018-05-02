# What happens when you click submit when update master
```
Creates a POST request and re-calls the `myimport` view.
May call some sort of multifile thing, but hopefully doesn't, idk what that does in this context
Opens `temp_csv_for_importing` and writes the file in there
calls `update_master` on `temp_csv_for_importing`
  Update_master does some formatting, then calls update or create for each entry in the csv with TITLE being the unique identifier.
```  
# What happens when you click submit when update page
```
Creates a POST request and re-calls the `myimport` view.
For each file in the request:
  Opens `temp_csv_for_importing` and writes the file in there
  calls `update_page` on `temp_csv_for_importing`
    Update_page does some formatting, generating a csv `temp_output.csv` then calls the main function in text_import.py (not to be confused with the `if __name__ == "__main__"` procedure)
      text_import has to build the tree thing we use, and make new entries for "WordAppearences"
```
