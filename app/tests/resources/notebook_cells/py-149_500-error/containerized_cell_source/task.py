from scipy.spatial import cKDTree
import numpy as np
import time

import argparse
import json
import os

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('--id', action='store', type=str, required=True,
                        dest='id')

args = arg_parser.parse_args()
print(args)

id = args.id


class FoxTree:
    def __init__(self, points_array, radius, vertical_resolution,
                 min_pts_per_cluster):
        """
    :param points_array: numpy array of shape (N, 3) containing x, y, z
    """
        self.radius = radius
        self.vertical_resolution = vertical_resolution
        self.min_pts_seeds = min_pts_per_cluster

        self.points_data = points_array
        self.num_pts = len(points_array)

        self.tree_ids = np.full(self.num_pts, -1, dtype=int)

        self.z_min = np.min(points_array[:, 2])
        self.z_max = np.max(points_array[:, 2])

        self.parsed_pt_indices = []  # List of indices
        self.next_tree_id = 0

        self.trees = {}

    def get_pts_in_layer(self, lower_z, higher_z):
        condition = (self.points_data[:, 2] > lower_z) & (
                    self.points_data[:, 2] <= higher_z)
        return np.where(condition)[0].tolist()

    def cluster_points(self, radius, pt_indices):
        clusters = []
        if not pt_indices:
            return clusters

        current_points = self.points_data[pt_indices]
        local_to_global = {i: pid for i, pid in enumerate(pt_indices)}
        kdtree = cKDTree(current_points)

        visited = set()
        pushed = set()

        for i in range(len(pt_indices)):
            global_idx = pt_indices[i]
            if global_idx in visited:
                continue

            curr_cluster = []
            stack = [i]
            pushed.add(i)

            while stack:
                curr_local_idx = stack.pop()
                curr_global_idx = local_to_global[curr_local_idx]

                if curr_global_idx not in visited:
                    curr_cluster.append(curr_global_idx)
                    visited.add(curr_global_idx)

                query_pt = current_points[curr_local_idx]
                neighbor_local_indices = kdtree.query_ball_point(query_pt,
                                                                 radius)

                for nb_local_idx in neighbor_local_indices:
                    if nb_local_idx not in pushed:
                        stack.append(nb_local_idx)
                        pushed.add(nb_local_idx)

            if len(curr_cluster) >= self.min_pts_seeds:
                clusters.append(curr_cluster)

        return clusters

    def assign_pts_to_trees(self, new_pt_ids, radius):
        rest_pt_ids = []
        if not self.parsed_pt_indices:
            return new_pt_ids

        parsed_points_data = self.points_data[self.parsed_pt_indices]
        parsed_tree = cKDTree(parsed_points_data)
        query_data = self.points_data[new_pt_ids]
        distances, indices = parsed_tree.query(query_data, k=1)

        for i, dist in enumerate(distances):
            pt_id = new_pt_ids[i]
            if dist < radius:
                nearest_parsed_idx = self.parsed_pt_indices[indices[i]]
                found_tree_id = self.tree_ids[nearest_parsed_idx]
                self.tree_ids[pt_id] = found_tree_id

                if found_tree_id not in self.trees:
                    self.trees[found_tree_id] = []
                self.trees[found_tree_id].append(pt_id)
                self.parsed_pt_indices.append(pt_id)
            else:
                rest_pt_ids.append(pt_id)
        return rest_pt_ids

    def generate_tree_clusters(self, pt_clusters):
        for cluster_indices in pt_clusters:
            current_id = self.next_tree_id
            self.next_tree_id += 1
            self.trees[current_id] = []
            for idx in cluster_indices:
                self.tree_ids[idx] = current_id
                self.trees[current_id].append(idx)

    def concatenate_to_parsed_pts(self, clusters):
        for cluster in clusters:
            self.parsed_pt_indices.extend(cluster)

    def separate_trees(self):
        print("Starting Top-Down Separation...")
        sep_start_time = time.time()
        is_top_layer, layer_idx = True, 0
        curr_height = self.z_max

        while curr_height >= self.z_min:
            t0 = time.time()
            pt_ids = self.get_pts_in_layer(
                curr_height - self.vertical_resolution, curr_height)

            if not pt_ids:
                curr_height -= self.vertical_resolution
                continue

            print(
                f"Layer {layer_idx}: Height [{curr_height - self.vertical_resolution:.2f} - {curr_height:.2f}], Points: {len(pt_ids)}")

            if is_top_layer:
                curr_layer_clusters = self.cluster_points(self.radius, pt_ids)
                self.generate_tree_clusters(curr_layer_clusters)
                self.concatenate_to_parsed_pts(curr_layer_clusters)
                if len(curr_layer_clusters) > 0:
                    is_top_layer = False
            else:
                rest_pts = pt_ids
                while True:
                    prev_parsed_count = len(self.parsed_pt_indices)
                    rest_pts = self.assign_pts_to_trees(rest_pts, self.radius)
                    if len(self.parsed_pt_indices) == prev_parsed_count:
                        break

                if rest_pts:
                    curr_layer_clusters = self.cluster_points(self.radius,
                                                              rest_pts)
                    self.generate_tree_clusters(curr_layer_clusters)
                    self.concatenate_to_parsed_pts(curr_layer_clusters)

            curr_height -= self.vertical_resolution
            layer_idx += 1

        print(
            f"Total Separation Algorithm Time: {time.time() - sep_start_time:.4f} seconds.")

    def output_trees(self, filename):
        print(f"Writing output to {filename}...")
        try:
            with open(filename, 'w') as f:
                for t_id, indices in self.trees.items():
                    r, g, b = np.random.randint(0, 255, 3)
                    for idx in indices:
                        pt = self.points_data[idx]
                        f.write(
                            f"{t_id} {pt[0]:.6f} {pt[1]:.6f} {pt[2]:.6f} {r} {g} {b}\n")
            print("Finished writing file.")
        except IOError as e:
            print(f"Error writing file: {e}")
