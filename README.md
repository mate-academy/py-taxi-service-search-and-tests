# Taxi service search and tests

- Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before start

In this task, you will implement search feature for your website and write tests for your project.

1. Implement search feature for all 3 pages with content:
   - drivers - by username        DONE
   - cars - by model              DONE
   - manufacturers - by name      DONE
2. Write tests for custom and for core project features (no need to test built-in functionality).
   Use this [tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing) as helper.
   You decide what to test and how to test (train your testing skills here).
3. Write tests for the searching feature that you have implemented. Make sure yourself, that it works as expected.

NOTE: Attach screenshots of all created pages to pull request. It's important to attach images not links to them.

# Note
Follow these steps if you need to use `crispy_forms` v2.0 with Python 3.11:

1. Add `CRISPY_TEMPLATE_PACK` to `settings.py`.

```python
CRISPY_TEMPLATE_PACK="bootstrap4"
```

2. Add these apps to `INSTALLED_APPS` and install them corresponding to the `CRISPY_TEMPLATE_PACK` bootstrap version.

```python
INSTALLED APPS = [
   ...,
   "crispy_bootstrap4",
   "crispy_forms",
]
```
