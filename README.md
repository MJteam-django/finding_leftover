# finding_leftover
Finding Leftover Ingredients at Local Restaurants


pip install django <br>
pip install djangorestframework <br>
pip install django-betterforms

library가 필요합니다:)

django-betterforms에 발생하는 에러는 <br>
관련 파일을<br>
```python
from six import python_2_unicode_compatible<br>
#from django.utils.encoding import python_2_unicode_compatible<br>
from six.moves import reduce<br>
```
로 수정해주시고 <br>
pip install six 해주시면 됩니다.<br>

감사합니다:)
