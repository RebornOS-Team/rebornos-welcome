{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. inheritance-diagram::
      {{ objname }}

|

.. autoclass:: {{ objname }}
   :members:    
   :undoc-members:
   :private-members:
   :special-members:                                
   :show-inheritance:                          
  
   {% block methods %}
   .. automethod:: __init__

   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}