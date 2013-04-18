#!/usr/bin/python
# coding=utf-8
import os
import codecs
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

tree = ET.ElementTree(file='blog.xml')

root = tree.getroot()

tag_channel=list(root)[0]

post_name = ""
post_previous_link = ""
post_previous_name = ""
post_title=""

for tag_item in tag_channel.iter():
    if tag_item.tag == 'item':
        post_previous_name = post_title
        post_type=list(tag_item)[17].text          #<wp:post_type>:post|attachment
        post_title = list(tag_item)[0].text        #<title> 
        post_id = list(tag_item)[8].text           #<wp:post_id>
        post_date = list(tag_item)[9].text         #<wp:post_date>
        post_content = list(tag_item)[6].text      #<content:encoded>
        post_status = list(tag_item)[14].text      #<wp:status>:publish|draft
        post_category = list(tag_item)[20].text    #category
        
        post_previous_link = post_name
        post_month = post_date.split('-')[0] + '/' + post_date.split('-')[1]
        
        post_name = post_month + '/' + post_title + ".html"    #example:2012/03/04/title.html
        indx_name = post_month + '/index.html'
        if post_type == 'post' and post_status == 'publish':
            post_tmpl_f = codecs.open("post_tmpl.html", "r", "utf-8")
            post_string = post_tmpl_f.read()
            post_tmpl_f.close()
            
            
            if os.path.isfile(indx_name):
                indx_tmpl_f = codecs.open(indx_name, "r", "utf-8")
            else:
                indx_tmpl_f = codecs.open("indx_tmpl.html","r","utf-8")
            indx_string = indx_tmpl_f.read()
            indx_tmpl_f.close()
            
            post_content = post_content.replace("\n","<br />")
            post_content = post_content.replace("'","\'")         #escape special characters
            post_string = post_string.replace("<![CDATA[TITLE]]>", post_title)
            post_string = post_string.replace("<![CDATA[PREVIOUS_LINK]]>", post_previous_link)
            post_string = post_string.replace("<![CDATA[PREVIOUS_NAME]]>", post_previous_name)
            post_string = post_string.replace("<![CDATA[PUBLISH_MONTH]]>", post_month)
            post_string = post_string.replace("<![CDATA[PUBLISH_DATE]]>", post_date)
            post_string = post_string.replace("<![CDATA[CONTENT]]>", post_content)
            post_string = post_string.replace("<![CDATA[CATEGORY]]>", post_category)
            
            indx_string = indx_string.replace("<![CDATA[TITLE]]>", post_title)
            indx_string = indx_string.replace("<![CDATA[POST_ID]]>", post_id)
            indx_string = indx_string.replace("<![CDATA[PUBLISH_MONTH]]>", post_month)
            indx_string = indx_string.replace("<![CDATA[PUBLISH_DATE]]>", post_date)
            indx_string = indx_string.replace("<![CDATA[POST_LINK]]>", "/posts/" + post_name)
            indx_string = indx_string.replace("<![CDATA[STRING_POSTED_ON]]>", "Posted on")
            indx_string = indx_string.replace("<![CDATA[STRING_POSTED_IN]]>", "Posted in")
            indx_string = indx_string.replace("<![CDATA[CATEGORY]]>", post_category)
            indx_string = indx_string.replace("<![CDATA[MONTH_CHINESE]]>", post_date.split('-')[0] +
                                              u"年" + str(int(post_date.split('-')[1])) + u"月")   #example:2012年3月
            indx_string = indx_string.replace("<![CDATA[CONTENT]]>", post_content[:140] + u"...<a href=\"/posts/" + post_name + u"\" title=\"Permalink to" + post_title + u"\" rel=\"bookmark\">阅读全文</a>")
            indx_string = indx_string.replace("<![CDATA[POST_ANCHOR]]>", u"<div id=\"post-<![CDATA[POST_ID]]>\" class=\"post-<![CDATA[POST_ID]]> post type-post status-publish format-standard hentry category-uncategorized\"><h2 class=\"entry-title\"><a href=\"<![CDATA[POST_LINK]]>\" title=\"Permalink to <![CDATA[TITLE]]>\" rel=\"bookmark\"><![CDATA[TITLE]]></a></h2><div class=\"entry-meta\"><span class=\"meta-prep meta-prep-author\"><![CDATA[STRING_POSTED_ON]]></span> <a href=\'/posts/<![CDATA[PUBLISH_MONTH]]>\' title=\"查看当月日志\" rel=\"bookmark\"><span class=\"entry-date\"><![CDATA[PUBLISH_DATE]]></span></a></div><!-- .entry-meta --><div class=\"entry-content\"><![CDATA[CONTENT]]></div><!-- .entry-content --><div class=\"entry-utility\"><span class=\"cat-links\"><span class=\"entry-utility-prep entry-utility-prep-cat-links\"><![CDATA[STRING_POSTED_IN]]></span> <a href=\"/category/<![CDATA[CATEGORY]]>/\" title=\"显示<![CDATA[CATEGORY]]>类别下的所有日志\" rel=\"category tag\"><![CDATA[CATEGORY]]></a></span></div><!-- .entry-utility --></div><!-- #post-## -->\n<![CDATA[POST_ANCHOR]]>")
            
            direcotry = os.path.dirname(post_name)
            if not os.path.exists(direcotry):
                os.makedirs(direcotry)
            out_posts = codecs.open(post_name, "w+", "utf-8")
            out_posts.write(post_string)
            out_posts.close()
            
            out_index = codecs.open(indx_name, "w+", "utf-8")
            out_index.write(indx_string)
            out_index.close()

