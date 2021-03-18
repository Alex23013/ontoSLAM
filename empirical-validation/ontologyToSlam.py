#!/usr/bin/env python
import os
import rospy
from std_msgs.msg import String

import math
from math import sin, cos, pi
import tf
from nav_msgs.msg import Odometry
from nav_msgs.msg import OccupancyGrid, MapMetaData
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL
import numpy as np

import os.path
from rdflib.plugins.sparql import prepareQuery

var_m = None
var_grid_list = None
flagMap = False

def get_position(g): 
    qpro = prepareQuery("""
                        PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
                        PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
                        PREFIX ns3:  <http://github.com/Alex23013/slam-up/FortesRey.owl#>
                        SELECT ?link ?rel ?o
                               WHERE {                                     
                                  ?robot a ns1:Robot .
                                  ?robot ns2:hasModel ?model .
                                  ?model ns2:hasPart ?link  .                            
                                  ?link  a ns2:BasePart .
                                  ?link ns2:hasPosition ?pos .
                                  ?pos ns2:hasTranslation ?t .
                                  ?t ?rel ?o   .
                                  FILTER ( ?o != ns3:cartesianPositionPoint )
                        }""" )
    pro = g.query(qpro)
    for row in pro:
        p = row[1]
        o = p[ p.find('#')+1: len(p)]
        if o == "cartesianX":
            px=float(row[2])
        if o == "cartesianY":
            py=float(row[2])
        if o == "cartesianZ":
            pz=float(row[2])
    return px,py,pz
    
def get_orientation(g): 
    qpro = prepareQuery("""
                        PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
                        PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
                        SELECT ?link ?rel ?o
                               WHERE {    
                                ?robot a ns1:Robot .
                                ?robot ns2:hasModel ?model .
                                ?model ns2:hasPart ?link  .                            
                                ?link  a ns2:BasePart .
                                ?link ns2:hasPosition ?pos .
                                ?pos ns2:hasOrientation ?t .
                   			    ?t a ns1:OrientationValue .
                                ?t ?rel ?o  .
                                FILTER ( ?o != ns1:OrientationValue )
                        }""" )
    orientation = g.query(qpro)
    for row in orientation:
        p = row[1]
        o = p[ p.find('#')+1: len(p)]
        if o == "componentX":
            ox=float(row[2])
        if o == "componentY":
            oy=float(row[2])
        if o == "componentZ":
            oz=float(row[2])
        if o == "componentW":
            ow=float(row[2])
    return ox,oy,oz,ow

def get_covar_matrix(g):
    qpro = prepareQuery("""
                        PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
                        PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
                        SELECT ?row ?col ?val
                               WHERE {    
                                ?robot a ns1:Robot .
                                ?robot ns2:hasModel ?model .
                                ?model ns2:hasPart ?link  .                            
                                ?link  a ns2:BasePart .
                                ?link ns2:hasPosition ?pos .
                                ?pos ns2:hasProbability ?t .
                   			    ?t ns2:hasMatrixValue ?mat .
                                ?ele ns2:belongs_to ?mat .
                                ?ele ns2:componentCol ?col .
                                ?ele ns2:componentRow ?row .
                                ?ele ns2:componentValue ?val 
                        }""" )
    pro = g.query(qpro)
    return pro


def get_stamp(g): 
    qpro = prepareQuery("""
                        PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
                        PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
                        SELECT ?stamp
                               WHERE {    
                                  ?robot a ns1:Robot .
                                  ?robot ns2:hasModel ?model .
                                  ?model ns2:hasPart ?link  .                            
                                  ?link  a ns2:BasePart .
                                  ?link ns2:hasPosition ?pos .
                                  ?pos ns2:posAtTime ?time .
                                  ?time ns2:hasStamp ?stamp
                        }""" )
    pro = g.query(qpro)
    return pro

def get_map_info(g): 
    qpro = prepareQuery("""
                        PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
                        PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
                        SELECT ?dim ?type ?val
                               WHERE {    
                                  ?env a ns1:Environment .
                                  ?env ns2:hasVisual ?vi .
                                  ?vi ns2:hasDimension ?dim .
                                  ?dim ns2:hasValue ?val .
                                  ?dim a ?type
                        }""" )
    pro = g.query(qpro)
    return pro

def get_map_resolution(g): 
    qpro = prepareQuery("""
                        PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
                        PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
                        SELECT ?val
                               WHERE {    
                                  ?env a ns1:Environment .
                                  ?env ns2:hasVisual ?vi .
                                  ?vi ns2:hasShape ?shape .
                                  ?shape ns2:has_resolution ?val 
                        }""" )
    pro = g.query(qpro)
    for row in pro:
        resolution = float(row[0])
    return resolution

def get_map_objects(g): 
    qpro = prepareQuery("""
                        PREFIX ns1: <http://www.semanticweb.org/ontologies/2013/7/CORA.owl#> 
                        PREFIX ns2:  <http://github.com/Alex23013/slam-up/OntoSLAM.owl#> 
                        SELECT ?obj ?val
                               WHERE {    
                                  ?env a ns1:Environment .
                                  ?obj a ns2:AtomicPart .
                                  ?joint ns2:hasChild ?obj .
                                  ?joint ns2:hasParent ?env .
                                  ?obj ns2:hasPosition ?pos .
                                  ?pos ns2:hasProbability ?prob .
                                  ?prob ns2:hasNumberValue ?val
                        }""" )
    pro = g.query(qpro)
    return pro



def talker():
    odom_pub = rospy.Publisher("odom1", Odometry, queue_size=50)
    map_pub = rospy.Publisher("map1", OccupancyGrid, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    
    odom_broadcaster = tf.TransformBroadcaster()
    #x = 0.0 
    #y = 0.0
    th = 0.0

    #vx = 0.1 
    #vy = -0.1
    vth = 0.1

    current_time = rospy.Time.now()
    last_time = rospy.Time.now()
    prefix = "out_turtle_map_"
    ext = ".owl"
    times = "1713" ## update init owl file
    file_input=prefix+times+ext
    
    r = rospy.Rate(1.0)
    while not rospy.is_shutdown():
        current_time = rospy.Time.now()
        g = Graph()
        '''
        #to Cloud
        print "file to download "+ file_input
        myCmd = 'gsutil -m cp gs://slam-up-bucket/'+file_input+' ./input'
        os.system(myCmd)
        local_file_input = 'input/'+file_input
        print "file que se va parsear "+local_file_input
        '''
        local_file_input = 'out/'+file_input ## INFO:: en el local 
        if os.path.exists(local_file_input):
            print "exist path "+local_file_input
            g.parse(local_file_input, format="turtle")
            print("graph has %s statements." % len(g))
            px,py,pz = get_position(g)
            ox,oy,oz,ow = get_orientation(g)
            matrix =  get_covar_matrix(g)
            
            covar = np.array([0.0]*36).reshape(6,6)
            for cell in matrix:
                row = int(cell[0])
                col = int(cell[1])
                value = float(cell[2])
                covar[row,col] = value
			
            covar_list = tuple(covar.ravel().tolist())
			
            #Creacion de nav_msg/Odometry
            # compute odometry in a typical way given the velocities of the robot
            '''dt = (current_time - last_time).to_sec()
            delta_x = (vx * cos(th) - vy * sin(th)) * dt
            delta_y = (vx * sin(th) + vy * cos(th)) * dt
            delta_th = vth * dt

            x += delta_x
            y += delta_y
            th += delta_th '''

            # since all odometry is 6DOF we'll need a quaternion created from yaw
            odom_quat =tf.transformations.quaternion_from_euler(0, 0, th)

            # first, we'll publish the transform over tf
            odom_broadcaster.sendTransform(
                (px, py, pz),
                odom_quat,
                current_time,
                "base_link1",
                "odom1"
            )

            # next, we'll publish the odometry message over ROS
            odom = Odometry()
            odom.header.stamp = current_time
            odom.header.frame_id = "odom1"

            # set the position
            odom.pose.pose = Pose(Point(px, py, pz),Quaternion(ox,oy,oz,ow))
            odom.pose.covariance = covar_list

            # set the velocity
            vx=vy=0 
            odom.child_frame_id = "base_link1"
            odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))

            odom_pub.publish(odom)

            ##map
            width=height=resolution=0
            mapa_info = get_map_info(g)
            if len(mapa_info) > 0:
                flagMap = True
            if flagMap is not True and var_m is not None and var_grid_list is not None:
                print "using saved"
                m = var_m
                grid_list = var_grid_list
            else:
                print "reading map"
                for row in mapa_info:
                    p = row[1]
                    o = p[ p.find('#')+1: len(p)]
                    if o == "Width":
                        width=int(row[2])
                    if o == "Height":
                        height=int(row[2])
                resolution = get_map_resolution(g)
                
                #Creacion de nav_msg/occupancyGrid
                len_grid = width * height
                grid_map = np.array([-1]*len_grid).reshape(width,height)
                objects = get_map_objects(g)
                print("objects detected")
                print(len(objects))
                for row in objects:
                    p = row[0]
                    obj_prefix ="http://github.com/Alex23013/slam-up/individual/obj/"
                    obj_pos = p[ len(obj_prefix): len(p)]
                    parts = obj_pos.split('_')
                    grid_map[int(parts[0]),int(parts[1])] = int(row[1])
                    
                grid_list = tuple(grid_map.ravel().tolist())
                
                map_broadcaster = tf.TransformBroadcaster()
                map_broadcaster.sendTransform(
                    (0,  0, 0),
                    odom_quat,
                    current_time,
                    "base_link1",
                    "map1"
                )

                m = MapMetaData()
                m.resolution = resolution
                m.width = width
                m.height = height
                pos = np.array([-width * resolution / 2, -height * resolution / 2, 0])
                quat = np.array([0, 0, 0, 1])
                m.origin = Pose()
                m.origin.position.x, m.origin.position.y = pos[:2]

            ogrid = OccupancyGrid()
            ogrid.header.frame_id = 'map1'
            ogrid.header.stamp = rospy.Time.now()

            ogrid.info = m
            ogrid.data = grid_list

            var_m = m
            var_grid_list = grid_list

            map_pub.publish(ogrid)
            rospy.loginfo("publishing map:") 
            rospy.loginfo(times)
            last_time = current_time
            
        else:
            print local_file_input,"file not found"
        rospy.loginfo("publishing odometry:") 
        rospy.loginfo(times)
        times = str(1+ int(times))
        file_input = prefix+times+ext
        print "antes sleep"
        r.sleep()
        print "fin_loop"

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass


                         
